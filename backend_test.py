#!/usr/bin/env python3
"""
Backend API Testing Script for Dhanyashree Portfolio
Tests all API endpoints for functionality and data integrity
"""

import requests
import json
import sys
from datetime import datetime
import os
from pathlib import Path

# Load environment variables to get the backend URL
def load_env_file(file_path):
    """Load environment variables from .env file"""
    env_vars = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value.strip('"')
    return env_vars

# Get backend URL from frontend .env
frontend_env = load_env_file('/app/frontend/.env')
BACKEND_URL = frontend_env.get('REACT_APP_BACKEND_URL', 'http://localhost:8001')
API_BASE = f"{BACKEND_URL}/api"

print(f"Testing backend at: {API_BASE}")
print("=" * 60)

class PortfolioAPITester:
    def __init__(self):
        self.passed_tests = 0
        self.failed_tests = 0
        self.test_results = []
        
    def log_test(self, test_name, passed, message="", response_data=None):
        """Log test result"""
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
        if message:
            print(f"   {message}")
        if response_data and not passed:
            print(f"   Response: {response_data}")
        print()
        
        self.test_results.append({
            "test": test_name,
            "passed": passed,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        
        if passed:
            self.passed_tests += 1
        else:
            self.failed_tests += 1
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if "status" in data and data["status"] == "healthy":
                    self.log_test("Health Check", True, "Health endpoint working correctly")
                    return True
                else:
                    self.log_test("Health Check", False, f"Invalid health response: {data}")
                    return False
            else:
                self.log_test("Health Check", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Health Check", False, f"Connection error: {str(e)}")
            return False
    
    def test_root_api_endpoint(self):
        """Test root API endpoint"""
        try:
            response = requests.get(f"{API_BASE}/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "Dhanyashree Portfolio API" in data["message"]:
                    self.log_test("Root API Endpoint", True, "Root endpoint working correctly")
                    return True
                else:
                    self.log_test("Root API Endpoint", False, f"Invalid root response: {data}")
                    return False
            else:
                self.log_test("Root API Endpoint", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Root API Endpoint", False, f"Connection error: {str(e)}")
            return False
    
    def test_portfolio_endpoint(self):
        """Test complete portfolio data endpoint"""
        try:
            response = requests.get(f"{API_BASE}/portfolio", timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                # Check required sections
                required_sections = ["personal_info", "education", "skills", "experience", "projects"]
                missing_sections = [section for section in required_sections if section not in data]
                
                if missing_sections:
                    self.log_test("Portfolio Data", False, f"Missing sections: {missing_sections}")
                    return False
                
                # Validate personal info
                personal_info = data["personal_info"]
                if personal_info.get("name") != "DHANYASHREE M V":
                    self.log_test("Portfolio Data", False, "Invalid personal info name")
                    return False
                
                # Validate projects count
                if len(data["projects"]) != 4:
                    self.log_test("Portfolio Data", False, f"Expected 4 projects, got {len(data['projects'])}")
                    return False
                
                self.log_test("Portfolio Data", True, f"Complete portfolio data with {len(data['projects'])} projects")
                return True
            else:
                self.log_test("Portfolio Data", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Portfolio Data", False, f"Error: {str(e)}")
            return False
    
    def test_skills_endpoint(self):
        """Test skills endpoint"""
        try:
            response = requests.get(f"{API_BASE}/skills", timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                # Check required skill categories
                required_categories = ["technical", "programming", "soft_skills"]
                missing_categories = [cat for cat in required_categories if cat not in data]
                
                if missing_categories:
                    self.log_test("Skills Data", False, f"Missing categories: {missing_categories}")
                    return False
                
                # Count total skills
                total_skills = len(data["technical"]) + len(data["programming"]) + len(data["soft_skills"])
                
                self.log_test("Skills Data", True, f"Skills categorized correctly with {total_skills} total skills")
                return True
            else:
                self.log_test("Skills Data", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Skills Data", False, f"Error: {str(e)}")
            return False
    
    def test_projects_endpoint(self):
        """Test projects endpoint"""
        try:
            response = requests.get(f"{API_BASE}/projects", timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                if not isinstance(data, list):
                    self.log_test("Projects Data", False, "Projects should be a list")
                    return False
                
                if len(data) != 4:
                    self.log_test("Projects Data", False, f"Expected 4 projects, got {len(data)}")
                    return False
                
                # Check project structure
                for i, project in enumerate(data):
                    required_fields = ["name", "subtitle", "description", "technologies"]
                    missing_fields = [field for field in required_fields if field not in project]
                    if missing_fields:
                        self.log_test("Projects Data", False, f"Project {i+1} missing fields: {missing_fields}")
                        return False
                
                project_names = [p["name"] for p in data]
                expected_projects = ["PURE FLOW", "DIAGNO-GENIE", "WILD GUARD AI", "OZONE LEVEL FORECASTING"]
                
                if set(project_names) != set(expected_projects):
                    self.log_test("Projects Data", False, f"Project names mismatch. Got: {project_names}")
                    return False
                
                self.log_test("Projects Data", True, f"All 4 projects returned with correct structure")
                return True
            else:
                self.log_test("Projects Data", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Projects Data", False, f"Error: {str(e)}")
            return False
    
    def test_experience_endpoint(self):
        """Test experience endpoint"""
        try:
            response = requests.get(f"{API_BASE}/experience", timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                if not isinstance(data, list):
                    self.log_test("Experience Data", False, "Experience should be a list")
                    return False
                
                if len(data) != 2:
                    self.log_test("Experience Data", False, f"Expected 2 experience entries, got {len(data)}")
                    return False
                
                # Check experience structure
                for i, exp in enumerate(data):
                    required_fields = ["title", "organization", "year", "responsibilities"]
                    missing_fields = [field for field in required_fields if field not in exp]
                    if missing_fields:
                        self.log_test("Experience Data", False, f"Experience {i+1} missing fields: {missing_fields}")
                        return False
                
                self.log_test("Experience Data", True, f"Experience data with {len(data)} entries returned correctly")
                return True
            else:
                self.log_test("Experience Data", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Experience Data", False, f"Error: {str(e)}")
            return False
    
    def test_education_endpoint(self):
        """Test education endpoint"""
        try:
            response = requests.get(f"{API_BASE}/education", timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                if not isinstance(data, list):
                    self.log_test("Education Data", False, "Education should be a list")
                    return False
                
                if len(data) != 2:
                    self.log_test("Education Data", False, f"Expected 2 education entries, got {len(data)}")
                    return False
                
                # Check education structure
                for i, edu in enumerate(data):
                    required_fields = ["degree", "institution", "branch", "duration"]
                    missing_fields = [field for field in required_fields if field not in edu]
                    if missing_fields:
                        self.log_test("Education Data", False, f"Education {i+1} missing fields: {missing_fields}")
                        return False
                
                self.log_test("Education Data", True, f"Education data with {len(data)} entries returned correctly")
                return True
            else:
                self.log_test("Education Data", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Education Data", False, f"Error: {str(e)}")
            return False
    
    def test_portfolio_stats_endpoint(self):
        """Test portfolio statistics endpoint"""
        try:
            response = requests.get(f"{API_BASE}/portfolio/stats", timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                required_fields = ["total_projects", "leadership_roles", "technologies", "contact_messages"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Portfolio Stats", False, f"Missing fields: {missing_fields}")
                    return False
                
                # Validate expected values
                if data["total_projects"] != 4:
                    self.log_test("Portfolio Stats", False, f"Expected 4 projects, got {data['total_projects']}")
                    return False
                
                if data["leadership_roles"] != 2:
                    self.log_test("Portfolio Stats", False, f"Expected 2 leadership roles, got {data['leadership_roles']}")
                    return False
                
                if data["technologies"] != 15:
                    self.log_test("Portfolio Stats", False, f"Expected 15 technologies, got {data['technologies']}")
                    return False
                
                self.log_test("Portfolio Stats", True, f"Stats: {data['total_projects']} projects, {data['technologies']} technologies, {data['contact_messages']} messages")
                return True
            else:
                self.log_test("Portfolio Stats", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Portfolio Stats", False, f"Error: {str(e)}")
            return False
    
    def test_contact_form_submission(self):
        """Test contact form submission"""
        try:
            # Test data
            contact_data = {
                "name": "Dhanyashree Test User",
                "email": "dhanyashree.test@example.com",
                "message": "This is a test message for the portfolio contact form. Testing backend API functionality."
            }
            
            response = requests.post(f"{API_BASE}/contact", json=contact_data, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check response structure
                required_fields = ["id", "name", "email", "message", "timestamp", "status"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Contact Form Submission", False, f"Response missing fields: {missing_fields}")
                    return False
                
                # Validate data integrity
                if data["name"] != contact_data["name"]:
                    self.log_test("Contact Form Submission", False, "Name mismatch in response")
                    return False
                
                if data["email"] != contact_data["email"]:
                    self.log_test("Contact Form Submission", False, "Email mismatch in response")
                    return False
                
                if data["message"] != contact_data["message"]:
                    self.log_test("Contact Form Submission", False, "Message mismatch in response")
                    return False
                
                if not data["id"]:
                    self.log_test("Contact Form Submission", False, "No ID generated")
                    return False
                
                self.log_test("Contact Form Submission", True, f"Contact message saved with ID: {data['id']}")
                return True
            else:
                self.log_test("Contact Form Submission", False, f"Status code: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_test("Contact Form Submission", False, f"Error: {str(e)}")
            return False
    
    def test_contact_form_validation(self):
        """Test contact form validation with invalid data"""
        try:
            # Test with missing fields
            invalid_data = {
                "name": "Test User"
                # Missing email and message
            }
            
            response = requests.post(f"{API_BASE}/contact", json=invalid_data, timeout=10)
            
            if response.status_code == 422:  # Validation error expected
                self.log_test("Contact Form Validation", True, "Properly rejects invalid data with 422 status")
                return True
            else:
                self.log_test("Contact Form Validation", False, f"Expected 422 for invalid data, got {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Contact Form Validation", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all backend tests"""
        print("Starting Backend API Tests...")
        print("=" * 60)
        
        # Test basic connectivity first
        if not self.test_health_endpoint():
            print("❌ Health check failed - backend may not be running")
            return False
        
        if not self.test_root_api_endpoint():
            print("❌ Root API endpoint failed - API routing may be broken")
            return False
        
        # Test portfolio data endpoints
        self.test_portfolio_endpoint()
        self.test_skills_endpoint()
        self.test_projects_endpoint()
        self.test_experience_endpoint()
        self.test_education_endpoint()
        self.test_portfolio_stats_endpoint()
        
        # Test contact form functionality
        self.test_contact_form_submission()
        self.test_contact_form_validation()
        
        # Print summary
        print("=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        print(f"📊 Total: {self.passed_tests + self.failed_tests}")
        
        if self.failed_tests == 0:
            print("\n🎉 All tests passed! Backend API is working correctly.")
            return True
        else:
            print(f"\n⚠️  {self.failed_tests} test(s) failed. Please check the issues above.")
            return False

if __name__ == "__main__":
    tester = PortfolioAPITester()
    success = tester.run_all_tests()
    
    # Save test results
    with open('/app/backend_test_results.json', 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "backend_url": API_BASE,
            "passed_tests": tester.passed_tests,
            "failed_tests": tester.failed_tests,
            "success": success,
            "test_results": tester.test_results
        }, f, indent=2)
    
    sys.exit(0 if success else 1)