$(document).ready(function () {
    // 1. Textillate Animations
    function initTextillate() {
        try {
            $('.text').textillate({
                loop: true,
                sync: true,
                in: { effect: "bounceIn" },
                out: { effect: "bounceOut" }
            });
        } catch (e) {
            console.log("Textillate warning:", e);
        }
    }

    initTextillate();

    // 2. Initialize SiriWave
    var siriWave = null;
    try {
        var container = document.getElementById("siri-container");
        if (container) {
            siriWave = new SiriWave({
                container: container,
                width: Math.min(window.innerWidth * 0.85, 800),
                height: 200,
                style: "ios9",
                amplitude: 1.2,
                speed: 0.25,
                autostart: true
            });
        }
    } catch (e) {
        console.log("SiriWave warning:", e);
    }

    // 3. UI Transition Functions exposed to Python via Eel
    eel.expose(ShowWave);
    function ShowWave() {
        $('#ovel').fadeOut(200, function () {
            $('#siriwave').fadeIn(200);
            if (siriWave) {
                siriWave.start();
                siriWave.setAmplitude(1.5);
            }
        });
    }

    eel.expose(ShowHood);
    function ShowHood() {
        $('#siriwave').fadeOut(200, function () {
            $('#ovel').fadeIn(200);
            if (siriWave) {
                siriWave.setAmplitude(0.4);
            }
        });
    }

    eel.expose(DisplayMessage);
    function DisplayMessage(message) {
        console.log("[Jarvis Display]:", message);
        $('.Siri-message').text(message);
        $('.assistant-status').text(message);

        if (siriWave) {
            var msg = message.toLowerCase();
            if (msg.includes("listening")) {
                siriWave.setAmplitude(2.2);
                siriWave.setSpeed(0.35);
            } else if (msg.includes("recognizing")) {
                siriWave.setAmplitude(1.0);
                siriWave.setSpeed(0.20);
            } else {
                siriWave.setAmplitude(1.5);
                siriWave.setSpeed(0.28);
            }
        }
    }

    // 4. Voice Input Trigger (Mic Button)
    $('#MicBtn').on('click', function (e) {
        e.preventDefault();
        ShowWave();
        DisplayMessage("Listening for your voice...");
        try {
            eel.allCommands(1)();
        } catch (err) {
            console.error("Eel call error:", err);
        }
    });

    // 5. Text Input Submission
    function submitChat() {
        var query = $('#chatbox').val().trim();
        if (query.length > 0) {
            $('#chatbox').val("");
            ShowWave();
            DisplayMessage(query);
            try {
                eel.allCommands(query)();
            } catch (err) {
                console.error("Eel call error:", err);
            }
        } else {
            $('#chatbox').focus();
        }
    }

    $('#ChatBtn').on('click', function (e) {
        e.preventDefault();
        submitChat();
    });

    $('#chatbox').on('keypress', function (e) {
        if (e.which === 13) {
            e.preventDefault();
            submitChat();
        }
    });

    // 6. Settings Modal
    $('#SettingBtn').on('click', function (e) {
        e.preventDefault();
        try {
            var myModal = new bootstrap.Modal(document.getElementById('settingsModal'));
            myModal.show();
        } catch (err) {
            $('#settingsModal').modal('show');
        }
    });

    // 7. Cancel / Return to Core
    $('#CancelWaveBtn').on('click', function (e) {
        e.preventDefault();
        ShowHood();
    });

    // 8. Hotkey: Ctrl + J or Space (when not typing in chatbox)
    $(document).on('keydown', function (e) {
        if (e.ctrlKey && e.key === 'j') {
            e.preventDefault();
            $('#MicBtn').click();
        }
    });
});