document.addEventListener('DOMContentLoaded', function() {
    // 必要なHTML要素を最初に取得しておく
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');
    const chatWindow = document.getElementById('chat-window');

    // フォームが送信されたときのイベント処理
    messageForm.addEventListener('submit', async function(e) {
        e.preventDefault(); // ページの再読み込みを防ぐ
        const userMessage = messageInput.value.trim();
        if (userMessage === '') return; // 空のメッセージは送信しない

        // 1. ユーザーのメッセージを即座にUIに追加
        appendMessage(userMessage, 'user', '/static/images/user.png');
        messageInput.value = ''; // 入力欄を空にする

        // 2. スピナーを表示
        const spinnerElement = showSpinner();

        try {
            // 3. サーバーに応答をリクエスト
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMessage })
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }
            
            const data = await response.json();
            
            // 4. AIの応答をUIに追加
            if (data.agent_message && data.agent_icon) {
                appendMessage(data.agent_message, 'agent', data.agent_icon);
            } else {
                throw new Error('Invalid response data from server.');
            }

        } catch (error) {
            console.error('An error occurred:', error);
            // エラーメッセージをUIに表示
            appendMessage('エラーが発生しました。しばらくしてからもう一度お試しください。', 'agent', '/static/images/ae.png');
        
        } finally {
            // 5. 成功しても失敗しても、必ず最後にスピナーを削除
            hideSpinner(spinnerElement);
        }
    });

    /**
     * スピナーを表示する関数
     */
    function showSpinner() {
        const container = document.createElement('div');
        container.id = 'spinner-message'; // 後で削除するためにIDを付与
        container.className = 'message agent';

        const icon = document.createElement('img');
        icon.src = '/static/images/ae.png';
        icon.className = 'chat-icon';
        
        const bubble = document.createElement('div');
        bubble.className = 'spinner-bubble';

        const spinner = document.createElement('div');
        spinner.className = 'spinner';
        
        bubble.appendChild(spinner);
        container.appendChild(icon);
        container.appendChild(bubble);
        chatWindow.appendChild(container);
        chatWindow.scrollTop = chatWindow.scrollHeight;
        return container; // 作成した要素を返す
    }

    /**
     * スピナーを削除する関数
     * @param {HTMLElement} element - 削除対象のスピナー要素
     */
    function hideSpinner(element) {
        if (element) {
            element.remove();
        }
    }
    
    /**
     * チャットウィンドウに新しいメッセージを追加する関数
     * @param {string} text - 表示するメッセージテキスト
     * @param {string} sender - 'user' または 'agent'
     * @param {string} iconPath - アイコンへのパス
     */
    function appendMessage(text, sender, iconPath) {
        const container = document.createElement('div');
        container.className = `message ${sender}`;

        const icon = document.createElement('img');
        icon.src = iconPath;
        icon.className = 'chat-icon';

        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        bubble.textContent = text;
        
        container.appendChild(icon);
        container.appendChild(bubble);
        chatWindow.appendChild(container);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }
});