import React, { useState, useEffect } from "react";
import axios from "axios";

const Category = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        //  Use your correct backend endpoint
        const res = await axios.get("http://192.168.29.134:5001");

        console.log("API Response:", res.data);

        //  Handle both direct array or wrapped in an object
        const data = Array.isArray(res.data)
          ? res.data
          : res.data?.categories || res.data?.data || [];

        if (Array.isArray(data)) {
          setCategories(data);
        } else {
          throw new Error("Unexpected API format — not an array");
        }

      } catch (err) {
        console.error("Error fetching categories:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchCategories();
  }, []);

  //  Loading state
  if (loading)
    return <div className="text-center mt-6 text-gray-600">Loading...</div>;


  if (error)
    return (
      <div className="text-center text-red-600 mt-6">
        Error fetching categories: {error}
      </div>
    );

  if (!categories || categories.length === 0)
    return (
      <div className="text-center mt-6 text-gray-500">
        No categories found.
      </div>
    );

  return (
    <div className="container mx-auto px-4 py-4">
      <h1 className="text-2xl font-extrabold text-gray-800 mb-6 text-left ">
        Categories
      </h1>

      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-6">
  {categories.map((cat) => (
    <div
      key={cat._id || cat.id}
      className="bg-white  overflow-hidden hover:shadow-lg transition-transform duration-300 hover:scale-105"
    >
      <div className=" w-fit h-3/4 "> 
        <img
          src={cat.image}
          alt={cat.categoryName}
          className="w-full h-full rounded-xl object-cover"
          onError={(e) =>
            (e.target.src =
              "https://via.placeholder.com/300x200?text=No+Image")
          }
        />
      </div>

      <div className="py-6 text-center">
        <h2 className="text-sm sm:text-base font-semibold text-gray-800 truncate">
          {cat.categoryName || "Unnamed Category"}
        </h2>
      </div>
    </div>
  ))}
</div>

    </div>
  );
};

export default Category;
