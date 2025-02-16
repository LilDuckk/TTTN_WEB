{
    const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    const room = playerInfo.dataset.code
    socket.emit('join', {room})

    socket.on('refresh', data=>{
        const curr_id = parseInt(playerInfo.dataset.current_db_id, 10)
        if(curr_id === data.last_player){
            location.reload()
        }

    })

    socket.on('gameover', data=>{
        const board = document.querySelector('#board')

        go_msg = document.createElement('div')
        go_msg.classList.add('go_msg')
        go_msg.innerHTML = `
            <p>${data.msg}</p>
            <a href='/'>Ok</a>
        `;

        board.appendChild(go_msg);

    })
}