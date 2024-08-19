document.addEventListener('DOMContentLoaded', function() {
    const calculatorForm = document.getElementById('calculator-form');
    const resultDisplay = document.getElementById('result-display');
    const clearDataButton = document.getElementById('clear-data');

    if (calculatorForm) {
        calculatorForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const weight = document.getElementById('weight').value;

            fetch('/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({weight: weight}),
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Received data:', data); // Log the received data
                updateTable(data);
                resultDisplay.textContent = '計算完成，請查看表格結果。';
                resultDisplay.style.display = 'block';
            })
            .catch((error) => {
                console.error('Error:', error);
                resultDisplay.textContent = '計算出錯，請稍後再試。';
                resultDisplay.style.display = 'block';
            });
        });
    }

    if (clearDataButton) {
        clearDataButton.addEventListener('click', clearData);
    }

    function clearData() {
        // Reset the form fields
        calculatorForm.reset();

        // Hide the result display
        resultDisplay.style.display = 'none';

        // Clear the calculated values in the table
        const calculatedValues = document.querySelectorAll('.calculated-value');
        calculatedValues.forEach(element => {
            element.textContent = '';
        });
    }

    function updateTable(data) {
        const table = document.getElementById('medicines-table');
        const rows = table.getElementsByTagName('tr');

        for (let i = 1; i < rows.length; i++) {
            const row = rows[i];
            const drugCode = row.cells[0].textContent;
            const results = data[drugCode];

            if (results) {
                row.cells[8].textContent = results.daily_max_ml;
                row.cells[9].textContent = results.single_dose_min_ml;
                row.cells[10].textContent = results.single_dose_max_ml;
            } else {
                row.cells[8].textContent = '';
                row.cells[9].textContent = '';
                row.cells[10].textContent = '';
            }
        }
    }

    // 添加一個簡單的動畫效果
    // Add a simple animation effect
    const title = document.querySelector('h1');
    if (title) {
        title.addEventListener('mouseover', function() {
            this.style.color = '#ff6b6b';
        });
        title.addEventListener('mouseout', function() {
            this.style.color = '#333';
        });
    }
});

// 添加一個簡單的返回頂部功能
// Add a simple back to top feature
window.onscroll = function() {
    const backToTopButton = document.getElementById('back-to-top');
    if (backToTopButton) {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            backToTopButton.style.display = "block";
        } else {
            backToTopButton.style.display = "none";
        }
    }
};

function scrollToTop() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}
