// React.Component are just classes that inherit from React.Component
// React.Component needs to return a React createElement
// needs to implement render() method, 
// render method triggered by setState() which changes 
// the value/state of special attribute state {dict}
class ClickButton extends React.Component {
  state = {
    wasClicked: false
  }

  handleClick () {
    this.setState(
      {wasClicked: true}
    )
  }

  render () {
    let buttonText

    if (this.state.wasClicked)
      buttonText = 'Clicked!'
    else
      buttonText = 'Click Me'
    // arg1, type of element e.g button
    // arg2, dict of element properties, size, rendered into the <class> html element
    // arg3, content of element, e.g. text
    return React.createElement(
      //1
      'button',
      //2
      {
        className: 'btn btn-primary mt-2',
        onClick: () => {
          this.handleClick()
        }
      },
      //3
      buttonText
    )
  }
}

// To mount a component onto the page (or the DOM) 
// we use the ReactDOM.render() function.
// DOM stands for Document Object Model 
// and is a way of representing the HTML page (document) as a tree of objects.

const domContainer = document.getElementById('react_root')
// ReactDOM.render() takes two arguments: 
// 1 a react element to render,
// 2. a DOM element in which to render it.
ReactDOM.render(
  React.createElement(ClickButton),
  domContainer
)