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