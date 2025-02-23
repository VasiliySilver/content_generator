document.addEventListener('DOMContentLoaded', function() {
    // Получаем сохраненные task_ids из localStorage
    let taskIds = JSON.parse(localStorage.getItem('contentPlanTasks') || '[]');

    // Функция для сохранения task_id в localStorage
    function saveTaskId(taskId) {
        taskIds.push({
            id: taskId,
            timestamp: new Date().toISOString(),
            status: 'PENDING'
        });
        localStorage.setItem('contentPlanTasks', JSON.stringify(taskIds));
    }

    document.getElementById('content-plan-form').addEventListener('submit', async function(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const data = Object.fromEntries(formData.entries());

        try {
            const response = await fetch('/api/v1/content-plan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                const result = await response.json();
                // Сохраняем task_id в localStorage
                saveTaskId(result.task_id);
                // Перенаправляем на страницу с задачами
                window.location.href = `/api/v1/ui/content-plan/${result.task_id}`;
            } else {
                const error = await response.json();
                alert('Failed to create content plan: ' + error.detail);
            }
        } catch (error) {
            alert('Error creating content plan: ' + error.message);
        }
    });

    document.getElementById('generate-articles').addEventListener('click', async function() {
        const planId = this.dataset.planId;
        try {
            const response = await fetch('/api/v1/articles/sequential', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ plan: planId })
            });

            if (response.ok) {
                const result = await response.json();
                saveTaskId(result.task_id);
                window.location.href = `/api/v1/ui/task/${result.task_id}`;
            } else {
                const error = await response.json();
                alert('Failed to start articles generation: ' + error.detail);
            }
        } catch (error) {
            alert('Error generating articles: ' + error.message);
        }
    });

    // Добавляем список последних задач на страницу
    const tasksContainer = document.createElement('div');
    tasksContainer.innerHTML = `
        <h3>Recent Content Plan Tasks</h3>
        <ul id="recent-tasks"></ul>
    `;
    document.querySelector('#content-plan-form').after(tasksContainer);

    // Функция для обновления списка задач
    function updateTasksList() {
        const tasksList = document.getElementById('recent-tasks');
        if (!tasksList) return;

        // Сортируем задачи по времени создания (новые сверху)
        const sortedTasks = [...taskIds].sort((a, b) => 
            new Date(b.timestamp) - new Date(a.timestamp)
        );

        tasksList.innerHTML = sortedTasks.map(task => `
            <li>
                <a href="/api/v1/ui/content-plan/${task.id}">
                    Task ${task.id.slice(0, 8)}... (${task.status})
                </a>
                <span class="timestamp">${new Date(task.timestamp).toLocaleString()}</span>
            </li>
        `).join('');
    }

    // Обновляем статусы задач каждые 5 секунд
    async function updateTaskStatuses() {
        for (let task of taskIds) {
            try {
                const response = await fetch(`/api/v1/task/${task.id}`);
                if (response.ok) {
                    const result = await response.json();
                    task.status = result.status;
                }
            } catch (error) {
                console.error('Error updating task status:', error);
            }
        }
        localStorage.setItem('contentPlanTasks', JSON.stringify(taskIds));
        updateTasksList();
    }

    // Инициализируем список задач и запускаем периодическое обновление
    updateTasksList();
    setInterval(updateTaskStatuses, 5000);
});
