for(let i = 0; i < 10; i += 1) {
  console.log('for loop i: ' + i)
}

let j = 0
while(j < 10) {
  console.log('while loop j: ' + j)
  j += 1
}

let k = 10

do {
  console.log('do while k: ' + k)
} while(k < 10)

const numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
// value is the function being returned for each number in array
// forEach only for arrays, 
// function to call by forEach number returned by => arrow function
// numbers.forEach(value()), when arbitrary functionName is value
numbers.forEach((functionName => {
  console.log('For each value func' + functionName)
}))
/* 
const numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
numbers.forEach((value => {
  console.log('For each value ' + value)
}))
*/
const doubled = numbers.map(value => value * 2)

console.log('Here are the doubled numbers')

console.log(doubled)
/*
function sayHello(yourName) {
  if (yourName === undefined) {
      console.log('Hello, no name')
  } else {
       console.log('Hello, ' + yourName)
  }
}
sayHello()
const yourName = 'Your Name'  // Put your name here

console.log('Before setTimeout')

setTimeout(() => {
    sayHello(yourName)
  }, 2000
)

console.log('After setTimeout')


Here we’re defining an anonymous function ()
that takes no arguments (the empty parentheses () before the =>), 

and immediately passing it to setTimeout(). 
When it’s called, 
it accesses the name variable from the outer scope, 
and passes it to sayHello().

 */