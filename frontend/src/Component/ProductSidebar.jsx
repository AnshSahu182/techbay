import React, { useState } from "react";
import Slider from "@mui/material/Slider";
import ProductsProduct from "./ProductsProduct";

const ProductSidebar = () => {
  const [priceRange, setPriceRange] = useState([500, 50000]); // initial price range

  // Function to handle slider movement
  const handlePriceChange = (event, newValue) => {
    setPriceRange(newValue);
  };

  // Show price value for accessibility
  const valuetext = (value) => `${value}₹`;

  return (
    <div className="flex flex-row m-5">
      
      <div className="border border-gray-200 shadow-md w-64 p-5 rounded-lg bg-white">


        <div className="flex flex-row justify-between items-center mb-4">
          <h1 className="font-semibold text-gray-700">Filter By</h1>
          <button
            className="text-blue-600 text-sm hover:underline"
            onClick={() => setPriceRange([1000, 50000]) }
          >
            Clear All
          </button>
        </div>

        
        <div className="mb-6">
          <h2 className="font-medium text-gray-800 mb-2">Price Range</h2>
          <Slider
            getAriaLabel={() => "Price range"}
            value={priceRange}
            onChange={handlePriceChange}
            valueLabelDisplay="auto"
            getAriaValueText={valuetext}
            min={0}
            max={100000}
            step={500}
            sx={{
              color: "#2563eb", // Tailwind's blue-600
            }}
          />
          <div className="flex justify-between text-sm text-gray-500 mt-1">
            <span>₹{priceRange[0]}</span>
            <span>₹{priceRange[1]}</span>
          </div>
        </div>

        
        <div className="mb-6">
          <h2 className="font-semibold text-gray-900 mb-2">Category</h2>
          {["Laptop", "Mobile", "Tablet", "Speaker", "Watch", "Camera"].map(
            (item) => (
              <label key={item} className="flex items-center gap-2 mb-1">
                <input type="checkbox"    className="accent-blue-600  cursor-pointer checked:border-blue-400
               checked:ring-2 " />
                <span>{item}</span>
              </label>
            )
          )}
        </div>

        
        <div>
          <h2 className="font-semibold text-gray-900 mb-2">Brand</h2>
          {["Apple", "Samsung", "Dell", "HP", "Sony", "Boat"].map((item) => (
            <label key={item} className="flex items-center gap-2 mb-1">
              <input type="checkbox" className="accent-blue-600" />
              <span>{item}</span>
            </label>
          ))}
        </div>
      </div>

      <div className="flex-1 ml-5">
        <ProductsProduct />
      </div>
    </div>
  );
};

export default ProductSidebar;
