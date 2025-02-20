{
    const buildInput = document.querySelector('#build_input');
    let buildCount = 0;
    let currentMoney = parseInt(playerInfo.dataset.current_player_money, 10);

    tiles.forEach(tile => tile.addEventListener('dblclick', e => {
        if (e.target.dataset.owner_id === playerInfo.dataset.current_player_index) {
            if (parseInt(e.target.dataset.build_price, 10) < currentMoney) {
                if (buildCount < 3) {
                    if (e.target.dataset.build != 'h') {
                        if (!buildInput.value.split(';').includes(e.target.dataset.id)) {
                            console.log('added');
                            buildInput.value += e.target.dataset.id + ';';
                            e.target.style = 'border: 3px solid green';  // Thêm vòng xanh quanh ô đất
                            buildCount++;
                            currentMoney -= parseInt(e.target.dataset.build_price, 10);
                            updateMoneyInfo(currentMoney);
                            updateBuyForm(currentMoney);
                        } else {
                            console.log('removed');
                            buildInput.value = buildInput.value.split(';').filter(id => id != e.target.dataset.id).join(';');
                            e.target.style = '';  // Xóa vòng xanh quanh ô đất
                            buildCount--;
                            currentMoney += parseInt(e.target.dataset.build_price, 10);
                            updateMoneyInfo(currentMoney);
                            updateBuyForm(currentMoney);
                        }
                    }
                }
            }
        }
    }));

    function updateMoneyInfo(money) {
        const className = `.player${playerInfo.dataset.current_player_index}_money`;
        document.querySelector(className).textContent = money;
        playerInfo.dataset.current_player_money = money;
    }

    function updateBuyForm(money) {
        if (money <= playerInfo.dataset.current_field_price) {
            br_yes.removeAttribute('checked');
            br_yes.setAttribute('disabled', '1');
            br_no.setAttribute('checked', '1');
        } else {
            br_yes.removeAttribute('disabled');
        }
    }
}