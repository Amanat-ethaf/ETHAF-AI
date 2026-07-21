// =====================================
// ETHAF AI - Final Professional Frontend
// Powered by Amanat
// =====================================

// ===== Elements =====

const chat = document.getElementById("chat");
const input = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");

// ===== Flask API Address =====

const API_URL = "http://172.16.2.98:5000/chat";

// =====================================
// Add Message to Chat
// =====================================

function addMessage(text, type) {

    const div = document.createElement("div");

    div.className = type + "-message";

    div.textContent = text;

    chat.appendChild(div);

    // Auto scroll
    chat.scrollTop = chat.scrollHeight;
}

// =====================================
// Send Message to ETHAF AI
// =====================================

async function sendMessage() {

    const message = input.value.trim();

    if (message === "") return;

    // Show user message
    addMessage(message, "user");

    // Clear input
    input.value = "";

    // ===== Typing Indicator =====

    const typing = document.createElement("div");

    typing.className = "ai-message";

    typing.textContent = "ETHAF AI is typing...";

    chat.appendChild(typing);

    chat.scrollTop = chat.scrollHeight;

    try {

        const response = await fetch(API_URL, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })
        });

        // Remove typing indicator
        typing.remove();

        if (!response.ok) {
            throw new Error("Server Error");
        }

        const data = await response.json();

        // Show AI reply
        addMessage(
            data.reply || "No reply received",
            "ai"
        );

    } catch (error) {

        // Remove typing indicator
        typing.remove();

        addMessage(
            "❌ Cannot connect to ETHAF AI server.\n" +
            "Make sure Pydroid/Termux is running and Flask server is started.",
            "ai"
        );

        console.error("Connection Error:", error);
    }
}

// =====================================
// Send Button Click
// =====================================

sendBtn.addEventListener("click", sendMessage);

// =====================================
// Enter Key Support
// =====================================

input.addEventListener("keydown", function (e) {

    if (e.key === "Enter") {

        e.preventDefault();

        sendMessage();
    }
});

// =====================================
// Auto Focus on Page Load
// =====================================

window.onload = () => {

    input.focus();
};

// =====================================
// 3-Dot Dropdown Menu
// =====================================

function toggleMenu() {

    const menu = document.getElementById("dropdownMenu");

    menu.classList.toggle("show");
}

// =====================================
// Close Menu When Clicking Outside
// =====================================

window.addEventListener("click", function (e) {

    const menu = document.getElementById("dropdownMenu");

    const btn = document.querySelector(".menu-btn");

    // Ignore if menu not found
    if (!menu || !btn) return;

    // Close if clicked outside
    if (
        !menu.contains(e.target) &&
        !btn.contains(e.target)
    ) {
        menu.classList.remove("show");
    }
});

// =====================================
// Mobile UX Improvements
// =====================================

// Keep input visible on mobile keyboard
input.addEventListener("focus", () => {

    setTimeout(() => {

        chat.scrollTop = chat.scrollHeight;

    }, 300);
});

// Prevent accidental double send
let sending = false;

async function safeSend() {

    if (sending) return;

    sending = true;

    try {

        await sendMessage();

    } finally {

        sending = false;
    }
}

// Replace button action with safe version
sendBtn.removeEventListener("click", sendMessage);

sendBtn.addEventListener("click", safeSend);

// Replace Enter action with safe version
input.addEventListener("keydown", function (e) {

    if (e.key === "Enter") {

        e.preventDefault();

        safeSend();
    }
});

// =====================================
// ETHAF AI Frontend Ready
// =====================================

console.log("🚀 ETHAF AI Frontend Ready");