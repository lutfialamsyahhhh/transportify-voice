(function () {
    const ttsText = document.getElementById("ttsText");
    const speedSelect = document.getElementById("speedSelect");
    const voiceSelect = document.getElementById("voiceSelect");
    const generateButton = document.getElementById("generateTtsButton");
    const ttsAudio = document.getElementById("ttsAudio");
    const downloadButton = document.getElementById("downloadTtsButton");
    const ttsState = document.getElementById("ttsState");
    const outputFileName = document.getElementById("outputFileName");
    const voiceNote = document.getElementById("voiceNote");
    const ttsAlert = document.getElementById("ttsAlert");

    generateButton.addEventListener("click", generateSpeech);

    async function generateSpeech() {
        const text = ttsText.value.trim();
        if (!text) {
            Transportify.showAlert(ttsAlert, "Text input is required.", "danger");
            return;
        }

        Transportify.hideAlert(ttsAlert);
        setLoading(true);

        try {
            const response = await fetch("/api/tts/generate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    text,
                    speed: speedSelect.value,
                    voice: voiceSelect.value,
                }),
            });
            const payload = await response.json();
            if (!response.ok || !payload.success) {
                throw new Error(payload.error || "TTS generation failed");
            }

            renderOutput(payload.data);
            if (payload.data.warning) {
                Transportify.showAlert(ttsAlert, payload.data.warning, "info");
            }
        } catch (error) {
            Transportify.showAlert(ttsAlert, error.message, "danger");
        } finally {
            setLoading(false);
        }
    }

    function renderOutput(data) {
        const audioUrl = Transportify.cacheBust(data.audio_url);
        const playbackRate = Number(data.playback_rate || 1);
        ttsAudio.src = audioUrl;
        ttsAudio.defaultPlaybackRate = playbackRate;
        ttsAudio.playbackRate = playbackRate;
        outputFileName.textContent = buildOutputLabel(data);
        downloadButton.href = data.download_url;
        downloadButton.classList.remove("disabled");
        voiceNote.textContent = buildVoiceNote(data);
        ttsState.textContent = "Generated";
        ttsAudio.onloadedmetadata = () => {
            ttsAudio.playbackRate = playbackRate;
        };
        ttsAudio.play().catch(() => {});
    }

    function buildOutputLabel(data) {
        if (!data.duration_seconds) {
            return data.file_name;
        }

        return `${data.file_name} | ${data.duration_seconds}s`;
    }

    function buildVoiceNote(data) {
        const speedInfo = data.speed_factor
            ? `Speed profile: ${data.speed} (${data.speed_rate}, about ${data.speed_factor}x).`
            : "";
        const voiceInfo = data.voice_id ? `Voice: ${data.voice_id}.` : "";
        const engineInfo = data.engine ? `Engine: ${data.engine}.` : "";
        const durationInfo = data.original_duration_seconds && data.duration_seconds
            ? `Duration: ${data.original_duration_seconds}s -> ${data.duration_seconds}s.`
            : "";
        return [data.voice_note, voiceInfo, engineInfo, speedInfo, durationInfo].filter(Boolean).join(" ");
    }

    function setLoading(active) {
        generateButton.disabled = active;
        generateButton.innerHTML = active
            ? '<span class="spinner-border spinner-border-sm"></span> Generating'
            : '<i class="bi bi-play-circle-fill"></i> Generate Speech';
        ttsState.textContent = active ? "Generating" : "Idle";
    }
})();
