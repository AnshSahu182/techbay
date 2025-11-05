import React from "react";
import FeaturedProducts from "./FeaturedProducts";
import Category from "./Category";
import TrustedCompanies from "./TrustedCompanies";
import { useNavigate } from "react-router-dom";

const Header = () => {
const Navigate =useNavigate();

  return (
<>
    <div
      className="flex flex-col items-center justify-center text-center 
                 min-h-[60vh] sm:min-h-[70vh] md:min-h-[80vh] lg:min-h-[90vh] 
                 w-full bg-cover bg-center bg-no-repeat rounded-none p-4 sm:p-6 md:p-10 mt-6"
      style={{
        backgroundImage:
          'linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.6)), url("https://lh3.googleusercontent.com/aida-public/AB6AXuBem-AyRDPF-wM113SE88pej_6X5bxTcYsSJSc84lWRPLPZyhsDsmGv0JTSH5b8u8CGJldUbDH3Vwh1X1TIATJiz2owcct0DoVEgcZR1PITUDMclfi0L48PMU4YlqQFcHll6ruf5eMppYHdBiFKbt2-o1-QkwONtdRzCkwNfxkuhCm4ZzjcdlFCt2VW2EoXYgMeXnzRxLyUqG6VGOVzB2MCUXTR4xOiaJKlhrfL0IU_JwWvQs_M-FWg1x5SIHRrwTdjwym3ehKd1Bc")',
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      <div className="flex flex-col gap-2 px-2">
        <h1 className="text-white text-3xl sm:text-4xl md:text-6xl font-extrabold leading-tight drop-shadow-md">
          Mega Sale on Laptops
        </h1>
        <h2 className="text-white text-sm sm:text-base md:text-lg font-light">
          Up to 40% Off on Select Models
        </h2>
      </div>

      <button className="mt-6 flex items-center justify-center h-10 sm:h-12 px-6 rounded-lg 
                         bg-blue-600 text-white text-sm sm:text-base font-semibold 
                         hover:bg-blue-700 transition-colors"
                         onClick={()=>Navigate('/products')}>
        Shop Now
      </button>
    </div>
    <div>

    <Category></Category>
    <FeaturedProducts></FeaturedProducts>
    <TrustedCompanies></TrustedCompanies>
    </div>
    </>
  );
};

export default Header;
