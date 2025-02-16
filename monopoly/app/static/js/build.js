if ( window.history.replaceState ) {
  window.history.replaceState( null, null, window.location.href );
}
const tiles = document.querySelectorAll('.tile')
const display = document.querySelector('#display')
const playerInfo = document.querySelector('#player_info')
const br_no = document.querySelector('.br_no')
const br_yes = document.querySelector('.br_yes')
const fieldCard = document.querySelector('#field_card')
const cardBody = document.querySelector('.card-body')

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
{
    const calls = []

    const fetchFieldInfo = e => {
        const id = e.target.dataset.id
        const url = `/field_info/${id}`
        const call = setTimeout(() => {
            fetch(url)
                .then(blob => blob.json())
                .then(json => {
                    fieldCard.setAttribute('style', 'visibility:visible')

                    switch (json.type) {
                        case 'CITY':
                            const header = document.createElement('h5')
                            header.textContent = json.label
                            cardBody.appendChild(header)

                            const price = document.createElement('p')
                            price.textContent = `price: ${json.price}$`
                            cardBody.appendChild(price)

                            const b_price = document.createElement('p')
                            b_price.textContent = `build price: ${json.build_price}$`
                            cardBody.appendChild(b_price)

                            const pricing = document.createElement('ul')
                            pricing.innerHTML = `
                    <li>no houses: ${json.pricing['0']}$</li>
                    <li>one house: ${json.pricing['1']}$</li>
                    <li>two houses: ${json.pricing['2']}$</li>
                    <li>three houses: ${json.pricing['3']}$</li>
                    <li>four houses: ${json.pricing['4']}$</li>
                    <li>hotel: ${json.pricing['h']}$</li>
                `
                            cardBody.appendChild(pricing)
                            break;
                    }


                })
                .catch(err => console.log(err))
        }, 400)
        calls.push(call)

    }

    tiles.forEach(tile => {
        tile.addEventListener('mouseenter', fetchFieldInfo)

        tile.addEventListener('mouseout', () => {
            calls.forEach(call => clearTimeout(call))
            fieldCard.setAttribute('style', 'visibility:hidden')
            cardBody.innerHTML = ''
        })
    })
}