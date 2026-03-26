function initSearch() {
    let data = SEARCH_DATA

    const input = document.getElementById("search")
    if (!input) return

    input.oninput = function () {

        let q = this.value.toLowerCase().trim()

        if (q === "") {
            document.getElementById("results").innerHTML = ""
            return
        }

        let res = data.filter(x =>
            (x.title && x.title.toLowerCase().includes(q)) ||
            (x.text && x.text.toLowerCase().includes(q))
        )

        res.sort((a, b) => b.date - a.date)

        let ul = document.getElementById("results")
        ul.innerHTML = ""

        res.slice(0, 100).forEach(x => {
            let li = document.createElement("li")

            li.innerHTML =
                `<a href="${x.url}">${x.date} [${x.source}] ${x.title}</a>`

            ul.appendChild(li)
        })
    }
}

// DOM状態に応じて実行
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initSearch)
} else {
    initSearch()
}