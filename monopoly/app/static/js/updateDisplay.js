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
                        fieldOwner.textContent = '';
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