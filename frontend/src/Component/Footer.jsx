import React from "react";

const Footer = () => {
  return (
    <footer className="bg-gray-50 text-gray-700 border-t mt-10">
      {/* Wrapper to center & control width */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-10 lg:px-16 xl:px-24 py-10">
        {/* Responsive grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-8 text-center md:text-left">
          
          {/* About Section */}
          <div>
            <h3 className="font-semibold text-lg mb-3 text-gray-800">About Techbay</h3>
            <p className="text-sm text-gray-600">
              Your one-stop shop for the latest and greatest in electronics.
            </p>
          </div>

          {/* Customer Service */}
          <div>
            <h3 className="font-semibold text-lg mb-3 text-gray-800">Customer Service</h3>
            <ul className="space-y-1 text-sm text-gray-600">
              <li><a href="#">Contact Us</a></li>
              <li><a href="#">FAQ</a></li>
              <li><a href="#">Shipping & Returns</a></li>
              <li><a href="#">Track Order</a></li>
            </ul>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-semibold text-lg mb-3 text-gray-800">Quick Links</h3>
            <ul className="space-y-1 text-sm text-gray-600">
              <li><a href="#">My Account</a></li>
              <li><a href="#">Wishlist</a></li>
              <li><a href="#">Terms & Conditions</a></li>
              <li><a href="#">Privacy Policy</a></li>
            </ul>
          </div>

          {/* Contact Section */}
          <div>
            <h3 className="font-semibold text-lg mb-3 text-gray-800">Contact Us</h3>
            <p className="text-sm text-gray-600">Email: support@techbay.com</p>
            <p className="text-sm text-gray-600">Phone: (123) 456-7890</p>
          </div>
        </div>

        {/* Bottom Copyright */}
        <div className="text-center text-sm text-gray-500 mt-10 border-t pt-6">
          © 2025 Techbay. All rights reserved.
        </div>
      </div>
    </footer>
  );
};

export default Footer;
