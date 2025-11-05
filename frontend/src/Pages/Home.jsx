import React from 'react'
import Navbar from '../Component/Navbar'
import Header from '../Component/Header'
import Footer from '../Component/Footer'

const Home = () => {
  return (
 <div className="min-h-screen bg-white">
  <Navbar />

  <div className="mx-4 sm:mx-8 md:mx-16 lg:mx-24 xl:mx-32">
    <Header />
    <Footer />
  </div>
</div>

  )
}

export default Home;
