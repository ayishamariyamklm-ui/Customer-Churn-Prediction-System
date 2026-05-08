// =========================
// CUSTOMER CHURN JS LOGIC
// =========================

document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");
    const resultBox = document.querySelector(".result");

    // If no result box exists yet, create one
    let resultContainer;
    if (!resultBox) {
        resultContainer = document.createElement("div");
        resultContainer.classList.add("result");
        form.parentNode.appendChild(resultContainer);
    } else {
        resultContainer = resultBox;
    }

    // =========================
    // FORM SUBMIT HANDLER
    // =========================
    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        // Show loading state
        showLoading();

        try {
            const formData = new FormData(form);
            const data = {};

            formData.forEach((value, key) => {
                data[key] = value;
            });

            // Convert numeric fields
            if (data.tenure) data.tenure = parseFloat(data.tenure);
            if (data.MonthlyCharges) data.MonthlyCharges = parseFloat(data.MonthlyCharges);
            if (data.TotalCharges) data.TotalCharges = parseFloat(data.TotalCharges);

            // Send request to API
            const response = await fetch("/api/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                displayResult(result.data);
            } else {
                showError(result.message || "Prediction failed");
            }

        } catch (error) {
            console.error(error);
            showError("Something went wrong. Please try again.");
        }
    });


    // =========================
    // DISPLAY RESULT
    // =========================
    function displayResult(data) {
        const riskClass = getRiskClass(data.churn_risk);

        resultContainer.className = "result " + riskClass;

        resultContainer.innerHTML = `
            <h3>Prediction: ${data.prediction === 1 ? "Will Churn" : "Will Stay"}</h3>
            <p><strong>Probability:</strong> ${(data.churn_probability * 100).toFixed(2)}%</p>
            <p><strong>Risk Level:</strong> ${data.churn_risk}</p>
        `;
    }


    // =========================
    // SHOW ERROR
    // =========================
    function showError(message) {
        resultContainer.className = "result error";

        resultContainer.innerHTML = `
            <h3>Error</h3>
            <p>${message}</p>
        `;
    }


    // =========================
    // LOADING STATE
    // =========================
    function showLoading() {
        resultContainer.className = "result";

        resultContainer.innerHTML = `
            <p>⏳ Predicting... Please wait</p>
        `;
    }


    // =========================
    // RISK COLOR LOGIC
    // =========================
    function getRiskClass(risk) {
        if (risk === "High Risk") return "error";
        if (risk === "Medium Risk") return "warning";
        return "success";
    }

});