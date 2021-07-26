const portions = $("p.portion");
const nutrients = document.getElementsByClassName("nutrient");

for (let x=0; x < portions.length; x++){
    $(".portion_number").click(function(){
        console.log($("this"))
        for (let i = 0; i < nutrients.length; i++) {
            let nutrientNum = parseFloat(nutrients[i].textContent);
            console.log($(".portion_number").text())
        }
    });
};
