// Context/FilterContext.jsx
import React, { createContext, useState, useEffect } from "react";
import axios from "axios";

export const FilterContext = createContext();

export const FilterProvider = ({ children }) => {
  const [filters, setFilters] = useState({
    category: [],
    brand: [],
    priceRange: [0, 1000],
  });

  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);

  //  Fetch products whenever filters change
  useEffect(() => {
    const fetchProducts = async () => {
      setLoading(true);
      try {
        const params = {
          category: filters.category.join(","),
          brand: filters.brand.join(","),
          minPrice: filters.priceRange[0],
          maxPrice: filters.priceRange[1],
        };

        const res = await axios.get(
          "https://interepithelial-unlunate-colt.ngrok-free.dev/products",
          { params }
        );
        setProducts(res.data);
      } catch (error) {
        console.error("Error fetching products:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, [filters]); //  runs every time filters change

  return (
    <FilterContext.Provider value={{ filters, setFilters, products, loading }}>
      {children}
    </FilterContext.Provider>
  );
};
