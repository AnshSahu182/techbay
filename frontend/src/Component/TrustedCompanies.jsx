import React from "react";

const TrustedCompanies = () => {
  const companies = [
    { name: "Apple", logo: "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg" },
    { name: "Microsoft", logo: "https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg" },
    { name: "Facebook", logo: "https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg" },
     { name: "Nike", logo: "https://upload.wikimedia.org/wikipedia/commons/a/a6/Logo_NIKE.svg" },
  ];

  return (
    <section className="py-10">
      <div className="max-w-6xl mx-auto text-center px-4">
        <h2 className="text-xl sm:text-2xl font-semibold text-gray-800 mb-6">
          Trusted By 1000+ Companies
        </h2>

        <div className="flex flex-wrap justify-center items-center gap-10">
          {companies.map((company) => (
            <div
              key={company.name}
              className="w-20 sm:w-28 flex justify-center items-center  transition"
            >
              <img
                src={company.logo}
                alt={company.name}
                className="w-full h-auto object-contain"
              />
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default TrustedCompanies;
