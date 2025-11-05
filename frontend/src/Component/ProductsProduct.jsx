import React, { useEffect, useState } from "react";
import axios from "axios";

const ProductsProduct = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const res = await axios.get("http://192.168.29.134:5002/products");
        console.log("API Response:", res.data);

        if (Array.isArray(res.data)) {
          setProducts(res.data);
        } else if (Array.isArray(res.data.products)) {
          setProducts(res.data.products);
        } else {
          throw new Error("Invalid API response format");
        }

        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  if (loading) return <div className="text-center mt-10">Loading...</div>;

  if (error)
    return <div className="text-center text-red-600 mt-10">Error: {error}</div>;

  return (
    <div className="container mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold text-gray-800 mb-6 text-center">
        All Products
      </h1>

      {products.length > 0 ? (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6">
          {products.map((product) => (
            <div
              key={product._id}
              className="bg-white shadow-md rounded-xl overflow-hidden hover:shadow-lg transition-all duration-300"
            >
              <img
                src={product.image || "https://via.placeholder.com/300x200?text=No+Image"}
                alt={product.title}
                className="w-full h-56 object-cover"
              />
              <div className="p-4 text-center">
                <h2 className="text-lg font-semibold text-gray-800">
                  {product.title || "Unnamed Product"}
                </h2>
                <p className="text-gray-600 mt-1">
                  ${product.price ? product.price.toFixed(2) : "N/A"}
                </p>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-center text-gray-500">No products found.</p>
      )}
    </div>
  );
};

export default ProductsProduct;
