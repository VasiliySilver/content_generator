document.addEventListener('DOMContentLoaded', function() {
    const articleLinks = document.querySelectorAll('.article-link');
    const articleDetail = document.getElementById('article-detail');
    const closeButton = document.getElementById('close-detail');
    let activeArticle = null;

    // Функция для отображения статьи
    async function showArticle(articleId, clickedElement) {
        try {
            const response = await fetch(`/api/v1/ui/article/${articleId}`);
            if (response.ok) {
                const article = await response.json();
                
                // Обновляем активный элемент
                if (activeArticle) {
                    activeArticle.classList.remove('active');
                }
                clickedElement.classList.add('active');
                activeArticle = clickedElement;

                // Обновляем детали статьи
                document.getElementById('article-title').textContent = article.title;
                document.getElementById('article-author').textContent = `By ${article.author}`;
                if (article.created_at) {
                    document.getElementById('article-date').textContent = new Date(article.created_at).toLocaleDateString();
                }
                
                // Обрабатываем markdown контент
                const content = article.content || '';
                document.getElementById('article-content').innerHTML = content;

                // Показываем панель с деталями
                articleDetail.classList.remove('hidden');

                // На мобильных устройствах прокручиваем к деталям
                if (window.innerWidth <= 1024) {
                    articleDetail.scrollIntoView({ behavior: 'smooth' });
                }
            } else {
                const error = await response.json();
                showError('Failed to load article: ' + (error.detail || 'Unknown error'));
            }
        } catch (error) {
            showError('Error loading article: ' + error.message);
        }
    }

    // Функция для отображения ошибки
    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        
        // Удаляем предыдущее сообщение об ошибке, если оно есть
        const existingError = document.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        
        // Добавляем новое сообщение об ошибке
        document.querySelector('.articles-container').prepend(errorDiv);
        
        // Удаляем сообщение через 5 секунд
        setTimeout(() => errorDiv.remove(), 5000);
    }

    // Обработчики событий
    articleLinks.forEach(link => {
        link.addEventListener('click', async function(event) {
            event.preventDefault();
            const articleId = this.dataset.articleId;
            await showArticle(articleId, this);
        });
    });

    // Обработчик закрытия детального просмотра
    if (closeButton) {
        closeButton.addEventListener('click', function() {
            articleDetail.classList.add('hidden');
            if (activeArticle) {
                activeArticle.classList.remove('active');
                activeArticle = null;
            }
        });
    }

    // Добавляем стили для сообщений об ошибках
    const style = document.createElement('style');
    style.textContent = `
        .error-message {
            background-color: #f8d7da;
            color: #721c24;
            padding: 12px;
            border-radius: 4px;
            margin-bottom: 20px;
            animation: slideIn 0.3s ease-out;
        }

        @keyframes slideIn {
            from {
                transform: translateY(-20px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
    `;
    document.head.appendChild(style);
});
