document.addEventListener("DOMContentLoaded", function () {
    // ---- Rotating quotes for the bottom bubble ----
    const quoteSpan = document.getElementById("quote-text");
    const quotes = [
        "I wish you saw yourself, the way I see you.",
        "You’re doing better than you think.",
        "It’s okay to take a breath.",
        "Nothing you feel is ‘too much’ here."
    ];

    if (quoteSpan && quotes.length > 1) {
        let idx = 0;
        setInterval(() => {
            quoteSpan.style.opacity = 0;
            setTimeout(() => {
                idx = (idx + 1) % quotes.length;
                quoteSpan.textContent = `“${quotes[idx]}”`;
                quoteSpan.style.opacity = 1;
            }, 400);
        }, 10000);
    }
});