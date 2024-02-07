document.addEventListener("DOMContentLoaded", function () {
    const appContainer = document.getElementById("app");

    // Function to display expenses
    function displayExpenses(expenses) {
        const expensesList = document.createElement("ul");

        expenses.forEach(expense => {
            const listItem = document.createElement("li");
            listItem.textContent = `${expense.product} - ${expense.amount} - ${expense.why}`;
            expensesList.appendChild(listItem);
        });

        appContainer.innerHTML = "";
        appContainer.appendChild(expensesList);
    }

    // Fetch and display user's expenses
    axios.get("/expenses/{{ current_user }}")
        .then(response => {
            const expenses = response.data;
            displayExpenses(expenses);
        })
        .catch(error => {
            console.error("Error fetching expenses:", error);
        });
});
