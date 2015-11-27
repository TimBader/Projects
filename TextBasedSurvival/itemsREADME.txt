// Lines starting with '//' and no text will be ignored
// ~Rq That means this element is requried, not doing so will result in crash, till i make the game yell at you
// ~CbO That means this element can be ommited, meaning that this will not contain anything

//This is how you create items for the game

//-i ~Rq, This means a new item this must be in for the compiler to know this is a new item
//itemName: ~Rq, This is the singular name of the item's name
//itemPuralCase: ~CbO, this is the pural case of the item's name, If this is ommited than the pural version of the name is the same as the singular
//otherNameCount: ~CbO, this is the number of other names that the item can be known as, if this is ommited then there are no other names this item can go as
// IMPORTANT: The following two attributes must be repeated the same number of times as the otherNameCount attribute
//otherName: ~ These are the other singular names that the item can go by
//otherNamePuralCase: ~ These are the other pural names that the item can go by
//itemDescription: ~ Rq, This is the description of the item when you inspect it
//itemClass: ~ Rq, This is the class of item for when you are crafting, you can make your own classes
//-d ~ Rq, tells that this is the end of the section

//Item Example:
//-i
//itemName: Twine
//otherNameCount: 1
//otherName: String
//itemDescription: Meow Meow Meow
//itemClass: Material
//-d ~Rq, this ends this section


//This is how you make an item for crafting, some things are simular to item creating
// IMPORTANT: Make sure all the crafting sections are BELOW all the item sections, if not the compiler will have a hard time finding what item this goes to if it doesnt know it exists yet

//-c ~ Rq, This tells the compiler that this sect is for crafting
//craftForItem: ~ Rq, This tells the compiler what item this recipe is for
//craftDialogue: ~ CbO, this is the dialogue displayed during crafting.  If ommited then this item doesnt get a dialogue when crafted
//craftClassReq: ~ CbO, this be the required item class (tool) you need in the inventory to complete this recipe.  If ommited then this recipe does not require anouther type of item
//recipeElementAmount: ~ Rq, This is the amount of elements in your recipe
// IMPORTANT: The following two attributes must be repeated the same number of times as the craftRecipeAmount attribute
//elementName: Rq, The name of the item in the recipe
//elementNumRq: Rq, The amount of that item requried in the recipe
//recipeCreateAmount: ~ Rq, How many the recipe makes of that item
//craftOtherAmount: ~ CbE, the amount of other items created from this recipe
// IMPORTANT: The following two attributes must be repeated the same number of times as the craftOtherAmount attribute
//craftOtherName: The item's name that will be also be created
//craftOtherNum: The amount of the created new item per 1 craft
//-d ~Rq, this ends this section

//Crafting example:

//-c
//craftForItem: Stick
//craftDialogue: POOOOOP!!!
//craftClassReq: Knife
//recipeElementAmount: 2
//elementName: Rabbit
//elementNumRq: 2
//elementName: Cut Grass
//elementNumRq: 10
//recipeCreateAmount: 5
//craftOtherAmount: 1
//craftOtherName: Twine
//craftOtherNum: 3
//-d