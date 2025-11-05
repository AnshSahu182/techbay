import React from 'react'
import Navbar from '../Component/Navbar'
import ProductSidebar from '../Component/ProductSidebar'
import { useNavigate } from 'react-router-dom'

const Products = () => {
  
  const nav=useNavigate();
  return (
    <div>
      
      <Navbar></Navbar>
      <div className='"mx-4  sm:mx-8 md:mx-16 lg:mx-24 xl:mx-32'>
      <div>
        <button onClick={()=>nav('/')}>Home</button>
        /
        <button onClick={()=>nav('/products') }>Products</button>
           </div>
      <div  className='mx-4 my-3 font-extrabold text-3xl flex items-start '>Explore Our Products</div>
      <div className='mx-4 text-gray-700' >Find the best electronics from top brand</div>
      
      <ProductSidebar></ProductSidebar>
    </div>
      </div>
  )
}

export default Products
