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
{
    const calls = [];

    const fetchFieldInfo = e => {
        const id = e.target.dataset.id;
        const url = `/field_info/${id}`;
        const call = setTimeout(() => {
            fetch(url)
                .then(blob => blob.json())
                .then(json => {
                    const fieldInfo = document.getElementById('field-info');
                    const fieldLabel = document.getElementById('field-label');
                    const fieldPrice = document.getElementById('field-price');
                    const fieldOwner = document.getElementById('field-owner');
                    const fieldPricing = document.getElementById('field-pricing');

                    fieldLabel.textContent = `Ô: ${json.label}`;
                    fieldOwner.textContent = `Owner: ${json.owner ? json.owner.id : 'None'}`;

                    if (json.type === 'CITY') {
                        fieldPrice.textContent = `Price: ${json.price || 'N/A'}$`;
                        fieldPricing.innerHTML = `
                            <li>Không nhà: ${json.pricing['0']}$</li>
                            <li>1 Nhà: ${json.pricing['1']}$</li>
                            <li>2 Nhà: ${json.pricing['2']}$</li>
                            <li>3 Nhà: ${json.pricing['3']}$</li>
                            <li>4 Nhà: ${json.pricing['4']}$</li>
                            <li>Khách sạn: ${json.pricing['h']}$</li>
                        `;
                    } else if (json.type === 'TRAIN') {
                        fieldPrice.textContent = `Price: 400$`;
                        fieldPricing.innerHTML = '';
                    } else if (json.type === 'POWERPLANT') {
                        fieldPrice.textContent = `Price: 300$`;
                        fieldPricing.innerHTML = '';
                    } else if (json.type === 'JAIL' || json.type === 'START') {
                        fieldPrice.textContent = '';
                        fieldOwner.textContent = '';
                        fieldPricing.innerHTML = '';
                    } else {
                        fieldPrice.textContent = '';
                        fieldPricing.innerHTML = '';
                    }

                    fieldInfo.style.display = 'block';
                    const fieldInfoHeight = fieldInfo.offsetHeight;
                    const fieldInfoWidth = fieldInfo.offsetWidth;
                    const pageHeight = window.innerHeight;
                    const pageWidth = window.innerWidth;

                    let top = e.pageY + 10;
                    let left = e.pageX + 10;

                    if (top + fieldInfoHeight > pageHeight) {
                        top = e.pageY - fieldInfoHeight - 10;
                    }

                    if (left + fieldInfoWidth > pageWidth) {
                        left = e.pageX - fieldInfoWidth - 10;
                    }

                    fieldInfo.style.left = `${left}px`;
                    fieldInfo.style.top = `${top}px`;
                })
                .catch(err => console.log(err));
        }, 400);
        calls.push(call);
    };

    const hideFieldInfo = () => {
        calls.forEach(call => clearTimeout(call));
        const fieldInfo = document.getElementById('field-info');
        fieldInfo.style.display = 'none';
    };

    const tiles = document.querySelectorAll('.tile');
    tiles.forEach(tile => {
        tile.addEventListener('mouseenter', fetchFieldInfo);
        tile.addEventListener('mouseout', hideFieldInfo);
    });
}