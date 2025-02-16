{
    const buildInput = document.querySelector('#build_input');
    let buildCount = 0;
    let currentMoney = parseInt(playerInfo.dataset.current_player_money, 10);

    tiles.forEach(tile => tile.addEventListener('click', e => {
        if (!e.shiftKey) {
            if (e.target.dataset.owner_id === playerInfo.dataset.current_player_index) {
                if (parseInt(e.target.dataset.build_price, 10) < currentMoney) {
                    if (buildCount < 3) {
                        if (e.target.dataset.build != 'h') {
                            console.log('added')
                            buildInput.value += e.target.dataset.id + ';';
                            e.target.style = 'border: 3px solid blue';
                            buildCount++;
                            currentMoney -= parseInt(e.target.dataset.build_price, 10)
                            updateMoneyInfo(currentMoney)
                            updateBuyForm(currentMoney)
                        }
                    }

                }
            }
        }
    }))

    tiles.forEach(tile => tile.addEventListener('click', e => {
        if (e.shiftKey) {
            if (buildInput.value.split(';').includes(e.target.dataset.id)) {
                console.log('removed')
                buildInput.value = buildInput.value.split(';').filter(id => id != e.target.dataset.id).join(';')
                e.target.style = '';
                buildCount--;
                currentMoney += parseInt(e.target.dataset.build_price, 10)
                updateMoneyInfo(currentMoney)
                updateBuyForm(currentMoney)
            }
        }

    }))

    function updateMoneyInfo(money) {
        const className = `.player${playerInfo.dataset.current_player_index}_money`
        document.querySelector(className).textContent = money
        playerInfo.dataset.current_player_money = money
    }

    function updateBuyForm(money){
        if(money <= playerInfo.dataset.current_field_price){
            br_yes.removeAttribute('checked')
            br_yes.setAttribute('disabled', '1')
            br_no.setAttribute('checked', '1')
        }{
            br_yes.removeAttribute('disabled')
        }
    }
}