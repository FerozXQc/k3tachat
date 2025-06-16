import { useState } from 'react'
import '../assets/css/lp.css'
import box from '../assets/images/box.png' 
function LandingPage(){
    const [toggleLoginForm,setToggleLoginForm] = useState(true)
    return(<>
    <div className="lp_container">
        <img src={box} alt="" />
        <form action="">
        <span>K3tachat</span>
        <p>totally not copied from instagram</p>
        <input type="text" placeholder='Username' />
        <input type="text" placeholder='Email'/>
        <input type="text" placeholder='Password' />
        <button type='submit'>submit</button>
        {toggleLoginForm? <p>New User? <a onClick={()=>{setToggleLoginForm(false)}}>Sign Up!</a></p>: <p>Existing User? <a onClick={()=>{setToggleLoginForm(true)}}>Sign in!</a></p>}
    </form>
    </div>
    </>)
}

export default LandingPage