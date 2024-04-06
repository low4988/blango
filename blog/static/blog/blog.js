const theNumber = 1
let yourName = 'This shit is Benanas'

if (theNumber === 1) {
  let yourName = 'Your name'
  alert(yourName)// displays first when if===true with variable inside if scope
}

alert(yourName) // displays second as variable declared outside if scope

/*  
const theNumber = 1
let yourName = 'This shit is Benanas'

if (theNumber === 1) { // === also takes type of vars into account
  let yourName = 'Your name'
  alert(yourName)// displays first when if===true with variable inside if scope
}

alert(yourName) // displays second as variable declared outside if scope
*/

/*  
alert('Hello, world!')
Call the JavaScript alert(str) function 
which takes a single string argument, 
and displays it as an alert dialog box in the browser. 
*/


/*  
Variables in JavaScript,
- let, for variables whose value might change
- const, for variables whose value won’t. 
Like in Python, variables aren’t typed, so their types can be reassigned.

Declaring variables with var
You can also assign variables with the keyword var, 
but this is an old way of doing it and not recommended anyway. 
Variables assigned with var are not scoped like let and const, 
we'll see an example of this variable scoping shortly. 

const framework = 'Django'
const language = 'Python'
alert(framework + ' is written in ' + language)

const name = 'Ben'
let benCount = 0
if (name === 'Ben') {
    benCount = 1
}

alert('There is ' + benCount + ' Ben')

if statement. The if(condition) must have parentheses around it. 
For a single line if statement, curly braces are not required, but sometimes it can be preferable to always use them to be very clear which parts of the code are inside the if body.
Notice that we’re using triple-equals (===) to compare 
the variables in the condition. 

Using === means that the types of the items
being compared are taken into comparison. 
For example, in JavaScript we could compare the 
string '1' and number 1 with ==. 
'1' == 1 would evaluate to true, 
as JavaScript coerces them to the same type and then compares. 

With === type coercion doesn’t take place, so '1' === 1 is false.

-----
const pi = 3.14159
pi = 3  // trade accuracy for speed
const values can’t be reassigned.

-------
let fruitCount = 5
let fruitCount = 6
Here the variable fruitCount is not being reassigned, 
it’s being redefined, which is not allowed.
----

Variables defined with const are allowed to be mutated, 
so we could add items to an array or reassign values in an object

Objects are declared with curly braces {}, equivalent to Python’s dict
Arrays can be defined using square brackets [], equivalent to Python’s list 

This is valid:
Can change, as this does not change the reference to the variable
i.e does not reassign the variable (only changes content of variable)
•	Change the elements of constant array, []
•	Change the properties of constant object


const fruit = ['Apple', 'Banana']
fruit.push('Cherry')  // append 'Cherry' to the end of the `fruit` list

const fruitCount = {Apple: 0, 'Banana': 1}
fruitCount.Cherry = 2  // add new item to object
fruitCount['Cherry'] = 2  // is equivalent

const myFruit = 'Cherry'
fruitCount[myFruit] = 2 // is also equivalent

You’ll need to refresh the page in your browser after each change. 
If you don’t see a change, you might need to hold Shift/Control 
when refreshing (depending on your browser) 
to force a refresh of the JavaScript file.
*/

/* multiline comments and end with */
// single line comments