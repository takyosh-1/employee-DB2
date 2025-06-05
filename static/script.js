let currentEmployeeId = null;

document.addEventListener('DOMContentLoaded', function() {
    const employeeItems = document.querySelectorAll('.employee-item');
    const employeeForm = document.getElementById('employeeForm');
    const noSelection = document.getElementById('noSelection');
    const updateForm = document.getElementById('updateForm');

    employeeItems.forEach(item => {
        item.addEventListener('click', function() {
            employeeItems.forEach(i => i.classList.remove('selected'));
            
            this.classList.add('selected');
            
            currentEmployeeId = parseInt(this.dataset.id);
            
            loadEmployeeDetails(currentEmployeeId);
        });
    });

    updateForm.addEventListener('submit', function(e) {
        e.preventDefault();
        updateEmployee();
    });

    function loadEmployeeDetails(employeeId) {
        fetch(`/api/employee/${employeeId}`)
            .then(response => response.json())
            .then(employee => {
                if (employee.error) {
                    showMessage('従業員情報の取得に失敗しました', 'error');
                    return;
                }
                
                document.getElementById('name').value = employee.name;
                document.getElementById('furigana').value = employee.furigana;
                document.getElementById('birth_date').value = employee.birth_date;
                document.getElementById('employee_id').value = employee.employee_id;
                document.getElementById('department').value = employee.department;
                document.getElementById('employment_type').value = employee.employment_type;
                document.getElementById('prefecture').value = employee.prefecture;
                document.getElementById('city').value = employee.city;
                document.getElementById('address').value = employee.address;
                document.getElementById('retirement_date').value = employee.retirement_date;
                document.getElementById('last_work_date').value = employee.last_work_date;
                
                noSelection.style.display = 'none';
                employeeForm.style.display = 'block';
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage('従業員情報の取得に失敗しました', 'error');
            });
    }

    function updateEmployee() {
        if (!currentEmployeeId) {
            showMessage('従業員が選択されていません', 'error');
            return;
        }

        const formData = new FormData(updateForm);
        const employeeData = {};
        
        for (let [key, value] of formData.entries()) {
            employeeData[key] = value;
        }

        fetch(`/api/employee/${currentEmployeeId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(employeeData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showMessage('更新に失敗しました', 'error');
                return;
            }
            
            showMessage('従業員情報を更新しました', 'success');
            
            updateEmployeeListItem(currentEmployeeId, data);
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('更新に失敗しました', 'error');
        });
    }

    function updateEmployeeListItem(employeeId, employeeData) {
        const listItem = document.querySelector(`[data-id="${employeeId}"]`);
        if (listItem) {
            listItem.querySelector('.employee-name').textContent = employeeData.name;
            listItem.querySelector('.employee-department').textContent = employeeData.department;
            listItem.querySelector('.retirement-date').textContent = `退職予定: ${employeeData.retirement_date}`;
        }
    }

    function showMessage(message, type) {
        const existingMessage = document.querySelector('.success-message, .error-message');
        if (existingMessage) {
            existingMessage.remove();
        }

        const messageDiv = document.createElement('div');
        messageDiv.className = type === 'success' ? 'success-message' : 'error-message';
        messageDiv.textContent = message;

        const employeeDetails = document.querySelector('.employee-details');
        employeeDetails.insertBefore(messageDiv, employeeForm);

        setTimeout(() => {
            messageDiv.remove();
        }, 3000);
    }
});
