(function () {
    const recordButton = document.getElementById("recordButton");
    const recordMeter = document.getElementById("recordMeter");
    const recordingState = document.getElementById("recordingState");
    const audioUpload = document.getElementById("audioUpload");
    const analyzeButton = document.getElementById("analyzeButton");
    const audioPreview = document.getElementById("audioPreview");
    const asrAlert = document.getElementById("asrAlert");
    const predictionLabel = document.getElementById("predictionLabel");
    const confidenceScore = document.getElementById("confidenceScore");
    const confidenceBar = document.getElementById("confidenceBar");
    const probabilityList = document.getElementById("probabilityList");
    const waveformImage = document.getElementById("waveformImage");
    const mfccImage = document.getElementById("mfccImage");
    const modelStatus = document.getElementById("modelStatus");
    const historyTable = document.getElementById("historyTable");
    const refreshHistory = document.getElementById("refreshHistory");
    const responseAudio = document.getElementById("responseAudio");
    const voiceResponseText = document.getElementById("voiceResponseText");

    const steps = {
        capture: document.getElementById("stepCapture"),
        mfcc: document.getElementById("stepMfcc"),
        predict: document.getElementById("stepPredict"),
        tts: document.getElementById("stepTts"),
    };

    let audioContext = null;
    let processor = null;
    let mediaStream = null;
    let sourceNode = null;
    let recordedBuffers = [];
    let selectedAudioBlob = null;
    let selectedAudioName = "recording.wav";
    let isRecording = false;

    recordButton.addEventListener("click", toggleRecording);
    audioUpload.addEventListener("change", handleUpload);
    analyzeButton.addEventListener("click", analyzeSelectedAudio);
    refreshHistory.addEventListener("click", loadHistory);
    loadHistory();

    async function toggleRecording() {
        if (isRecording) {
            stopRecording();
            return;
        }

        try {
            Transportify.hideAlert(asrAlert);
            mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
            sourceNode = audioContext.createMediaStreamSource(mediaStream);
            processor = audioContext.createScriptProcessor(4096, 1, 1);
            recordedBuffers = [];

            processor.onaudioprocess = (event) => {
                recordedBuffers.push(new Float32Array(event.inputBuffer.getChannelData(0)));
            };

            sourceNode.connect(processor);
            processor.connect(audioContext.destination);
            isRecording = true;
            setRecordingUi(true);
            setStep("capture");
        } catch (error) {
            Transportify.showAlert(asrAlert, "Microphone permission is required for recording.", "danger");
        }
    }

    function stopRecording() {
        if (processor) {
            processor.disconnect();
        }
        if (sourceNode) {
            sourceNode.disconnect();
        }
        if (mediaStream) {
            mediaStream.getTracks().forEach((track) => track.stop());
        }

        const sampleRate = audioContext ? audioContext.sampleRate : 44100;
        const wavBlob = encodeWav(recordedBuffers, sampleRate);
        selectedAudioBlob = wavBlob;
        selectedAudioName = "recording.wav";
        audioPreview.src = URL.createObjectURL(wavBlob);
        analyzeButton.disabled = false;

        if (audioContext) {
            audioContext.close();
        }

        isRecording = false;
        setRecordingUi(false);
        recordingState.textContent = "Recorded";
    }

    function setRecordingUi(active) {
        recordButton.classList.toggle("is-recording", active);
        recordMeter.classList.toggle("active", active);
        recordingState.textContent = active ? "Recording" : "Ready";
        recordButton.setAttribute("aria-label", active ? "Stop recording" : "Start recording");
        recordButton.innerHTML = active ? '<i class="bi bi-stop-fill"></i>' : '<i class="bi bi-mic-fill"></i>';
    }

    function handleUpload(event) {
        const file = event.target.files[0];
        if (!file) {
            return;
        }
        selectedAudioBlob = file;
        selectedAudioName = file.name || "upload.wav";
        audioPreview.src = URL.createObjectURL(file);
        analyzeButton.disabled = false;
        recordingState.textContent = "Uploaded";
        setStep("capture");
    }

    async function analyzeSelectedAudio() {
        if (!selectedAudioBlob) {
            Transportify.showAlert(asrAlert, "Select or record audio before analysis.", "danger");
            return;
        }

        Transportify.hideAlert(asrAlert);
        analyzeButton.disabled = true;
        analyzeButton.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Analyzing';
        setStep("mfcc");

        const formData = new FormData();
        formData.append("audio", selectedAudioBlob, selectedAudioName);

        try {
            const response = await fetch("/api/asr/predict", {
                method: "POST",
                body: formData,
            });
            const payload = await response.json();

            if (!response.ok || !payload.success) {
                throw new Error(payload.error || "ASR prediction failed");
            }

            setStep("predict");
            renderPrediction(payload.data);
            await loadHistory();
            await generateVoiceResponse(payload.data.label);
        } catch (error) {
            Transportify.showAlert(asrAlert, error.message, "danger");
        } finally {
            analyzeButton.disabled = false;
            analyzeButton.innerHTML = '<i class="bi bi-stars"></i> Analyze Audio';
        }
    }

    function renderPrediction(data) {
        predictionLabel.textContent = data.label;
        confidenceScore.textContent = Transportify.formatPercent(data.confidence);
        confidenceBar.style.width = Transportify.formatPercent(data.confidence);
        modelStatus.textContent = data.demo ? "Demo fallback" : "Trained model";
        modelStatus.classList.toggle("muted", !data.demo);

        waveformImage.src = Transportify.cacheBust(data.waveform_url);
        mfccImage.src = Transportify.cacheBust(data.mfcc_url);

        const entries = Object.entries(data.probabilities || {})
            .sort((a, b) => b[1] - a[1]);

        probabilityList.innerHTML = entries.map(([label, probability]) => `
            <div>
                <span>${label}</span>
                <strong>${Transportify.formatPercent(probability)}</strong>
            </div>
        `).join("");

        if (data.demo) {
            Transportify.showAlert(asrAlert, "Demo fallback active: train the MFCC/SVM model when dataset recordings are ready.", "info");
        }
    }

    async function generateVoiceResponse(label) {
        setStep("tts");
        voiceResponseText.textContent = `Anda mengatakan ${label}`;

        try {
            const response = await fetch("/api/integrations/asr-to-tts", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ prediction: label, speed: "normal" }),
            });
            const payload = await response.json();
            if (!response.ok || !payload.success) {
                throw new Error(payload.error || "Voice response unavailable");
            }
            responseAudio.src = Transportify.cacheBust(payload.data.audio_url);
            responseAudio.play().catch(() => {});
        } catch (error) {
            Transportify.showAlert(asrAlert, `${error.message} The text response is still available.`, "info");
        }
    }

    async function loadHistory() {
        const response = await fetch("/api/asr/history");
        const payload = await response.json();
        const items = payload.data.items || [];

        if (!items.length) {
            historyTable.innerHTML = '<tr><td colspan="5" class="text-center text-secondary-light">No predictions yet</td></tr>';
            return;
        }

        historyTable.innerHTML = items.map((item) => {
            const createdAt = new Date(item.created_at).toLocaleString();
            const mode = item.demo ? "Demo" : "Trained";
            return `
                <tr>
                    <td>${createdAt}</td>
                    <td><strong>${item.label}</strong></td>
                    <td>${Transportify.formatPercent(item.confidence)}</td>
                    <td>${mode}</td>
                    <td>${item.source}</td>
                </tr>
            `;
        }).join("");
    }

    function setStep(activeKey) {
        Object.entries(steps).forEach(([key, element]) => {
            if (element) {
                element.classList.toggle("active", key === activeKey);
            }
        });
    }

    function encodeWav(buffers, sampleRate) {
        const samples = flattenBuffers(buffers);
        const buffer = new ArrayBuffer(44 + samples.length * 2);
        const view = new DataView(buffer);

        writeString(view, 0, "RIFF");
        view.setUint32(4, 36 + samples.length * 2, true);
        writeString(view, 8, "WAVE");
        writeString(view, 12, "fmt ");
        view.setUint32(16, 16, true);
        view.setUint16(20, 1, true);
        view.setUint16(22, 1, true);
        view.setUint32(24, sampleRate, true);
        view.setUint32(28, sampleRate * 2, true);
        view.setUint16(32, 2, true);
        view.setUint16(34, 16, true);
        writeString(view, 36, "data");
        view.setUint32(40, samples.length * 2, true);

        let offset = 44;
        for (let i = 0; i < samples.length; i += 1) {
            const sample = Math.max(-1, Math.min(1, samples[i]));
            view.setInt16(offset, sample < 0 ? sample * 0x8000 : sample * 0x7fff, true);
            offset += 2;
        }

        return new Blob([view], { type: "audio/wav" });
    }

    function flattenBuffers(buffers) {
        const length = buffers.reduce((total, buffer) => total + buffer.length, 0);
        const result = new Float32Array(length);
        let offset = 0;
        buffers.forEach((buffer) => {
            result.set(buffer, offset);
            offset += buffer.length;
        });
        return result;
    }

    function writeString(view, offset, string) {
        for (let i = 0; i < string.length; i += 1) {
            view.setUint8(offset + i, string.charCodeAt(i));
        }
    }
})();
