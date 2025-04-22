document.addEventListener("DOMContentLoaded", function () {
    const params = new URLSearchParams(window.location.search);

    if (params.get("register_success") === "True") {
        alert("✅ Registration successful! Please login.");

        // ✅ 移除 `register_success`，防止页面刷新后 `alert()` 再次弹出
        params.delete("register_success");
        window.history.replaceState({}, document.title, window.location.pathname);
    }

    // 发送 OTP 验证码
    document.getElementById("send-otp-btn")?.addEventListener("click", function () {
        console.log("1121332")
        let email = document.getElementById("email").value;
        if (!email.includes("@")) {
            alert("Please enter a valid email address!");
            return;
        }
        fetch("/send_otp", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: email })
        })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
            })
            .catch(error => console.error("Error:", error));
    });
});

