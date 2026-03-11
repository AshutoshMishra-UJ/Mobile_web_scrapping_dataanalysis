"""
Mobile Phone Recommendation System
Recommends phones based on user budget and preferences
"""

import pandas as pd
import numpy as np
import re
import warnings
warnings.filterwarnings('ignore')


class PhoneRecommendationSystem:
    def __init__(self, csv_file='smartprix_phones_data.csv'):
        """Initialize the recommendation system with phone data"""
        print("Loading phone data...")
        self.df = pd.read_csv(csv_file)
        self.clean_data()
        print(f"✓ Loaded {len(self.df)} phones successfully!\n")
    
    def clean_data(self):
        """Clean and preprocess the data for recommendations"""
        # Extract numeric price from price column (e.g., "₹15,999" -> 15999)
        self.df['price_numeric'] = self.df['price'].apply(self.extract_price)
        
        # Extract camera megapixels (take the main camera value)
        self.df['camera_mp'] = self.df['camera'].apply(self.extract_camera_mp)
        
        # Extract RAM in GB
        self.df['ram_gb'] = self.df['ram'].apply(self.extract_ram_gb)
        
        # Extract battery capacity in mAh
        self.df['battery_mah'] = self.df['battery'].apply(self.extract_battery)
        
        # Extract display size in inches
        self.df['display_inches'] = self.df['display'].apply(self.extract_display)
        
        # Convert rating to numeric (handle NaN)
        self.df['rating_numeric'] = pd.to_numeric(self.df['rating'], errors='coerce')
        
        # Create processor score (simplified - can be enhanced)
        self.df['processor_score'] = self.df['processor'].apply(self.score_processor)
        
        # Drop rows with missing price
        self.df = self.df[self.df['price_numeric'] > 0].copy()
        
    def extract_price(self, price_str):
        """Extract numeric price from string"""
        if pd.isna(price_str):
            return 0
        # Remove ₹, commas, and extract number
        match = re.search(r'[\d,]+', str(price_str))
        if match:
            return int(match.group().replace(',', ''))
        return 0
    
    def extract_camera_mp(self, camera_str):
        """Extract main camera megapixels"""
        if pd.isna(camera_str):
            return 0
        # Find all numbers followed by MP
        matches = re.findall(r'(\d+\.?\d*)\s*MP', str(camera_str))
        if matches:
            # Return the highest MP value (usually the main camera)
            return float(max(matches, key=float))
        return 0
    
    def extract_ram_gb(self, ram_str):
        """Extract RAM in GB"""
        if pd.isna(ram_str):
            return 0
        # Look for number followed by GB
        match = re.search(r'(\d+)\s*GB', str(ram_str))
        if match:
            return int(match.group(1))
        return 0
    
    def extract_battery(self, battery_str):
        """Extract battery capacity in mAh"""
        if pd.isna(battery_str):
            return 0
        # Look for number followed by mAh
        match = re.search(r'(\d+)\s*mAh', str(battery_str))
        if match:
            return int(match.group(1))
        return 0
    
    def extract_display(self, display_str):
        """Extract display size in inches"""
        if pd.isna(display_str):
            return 0
        # Look for decimal number followed by inch or "
        match = re.search(r'(\d+\.?\d*)\s*(?:inch|")', str(display_str))
        if match:
            return float(match.group(1))
        return 0
    
    def score_processor(self, processor_str):
        """Simple processor scoring based on keywords"""
        if pd.isna(processor_str):
            return 0
        
        processor_str = str(processor_str).lower()
        score = 50  # base score
        
        # Premium processors
        if 'snapdragon 8' in processor_str or 'dimensity 9' in processor_str:
            score += 50
        elif 'snapdragon 7' in processor_str or 'dimensity 8' in processor_str:
            score += 40
        elif 'snapdragon 6' in processor_str or 'dimensity 7' in processor_str:
            score += 30
        elif 'snapdragon' in processor_str or 'dimensity' in processor_str:
            score += 20
        elif 'helio' in processor_str:
            score += 15
        
        # Extract processor number if available
        match = re.search(r'(\d{3,4})', processor_str)
        if match:
            score += int(match.group(1)) / 50
            
        return score
    
    def filter_by_budget(self, max_price, min_price=0):
        """Filter phones within budget"""
        return self.df[(self.df['price_numeric'] >= min_price) & 
                       (self.df['price_numeric'] <= max_price)].copy()
    
    def recommend_by_camera(self, budget, top_n=5):
        """Recommend phones with best camera within budget"""
        filtered = self.filter_by_budget(budget)
        if len(filtered) == 0:
            return None
        
        # Sort by camera MP (descending) and rating
        filtered['score'] = (filtered['camera_mp'] * 0.7 + 
                           filtered['rating_numeric'].fillna(0) * 10)
        
        return filtered.nlargest(top_n, 'score')[
            ['model', 'price', 'camera', 'rating', 'camera_mp', 'price_numeric']
        ]
    
    def recommend_by_processor(self, budget, top_n=5):
        """Recommend phones with best processor within budget"""
        filtered = self.filter_by_budget(budget)
        if len(filtered) == 0:
            return None
        
        filtered['score'] = (filtered['processor_score'] * 0.7 + 
                           filtered['rating_numeric'].fillna(0) * 10)
        
        return filtered.nlargest(top_n, 'score')[
            ['model', 'price', 'processor', 'rating', 'processor_score', 'price_numeric']
        ]
    
    def recommend_by_ram(self, budget, top_n=5):
        """Recommend phones with best RAM within budget"""
        filtered = self.filter_by_budget(budget)
        if len(filtered) == 0:
            return None
        
        filtered['score'] = (filtered['ram_gb'] * 10 + 
                           filtered['rating_numeric'].fillna(0) * 5)
        
        return filtered.nlargest(top_n, 'score')[
            ['model', 'price', 'ram', 'rating', 'ram_gb', 'price_numeric']
        ]
    
    def recommend_by_battery(self, budget, top_n=5):
        """Recommend phones with best battery within budget"""
        filtered = self.filter_by_budget(budget)
        if len(filtered) == 0:
            return None
        
        filtered['score'] = (filtered['battery_mah'] / 100 + 
                           filtered['rating_numeric'].fillna(0) * 10)
        
        return filtered.nlargest(top_n, 'score')[
            ['model', 'price', 'battery', 'rating', 'battery_mah', 'price_numeric']
        ]
    
    def recommend_by_rating(self, budget, top_n=5):
        """Recommend highest rated phones within budget"""
        filtered = self.filter_by_budget(budget)
        if len(filtered) == 0:
            return None
        
        # Filter out phones without ratings
        filtered = filtered[filtered['rating_numeric'].notna()]
        
        if len(filtered) == 0:
            return None
        
        return filtered.nlargest(top_n, 'rating_numeric')[
            ['model', 'price', 'rating', 'processor', 'camera', 'ram', 'battery', 'price_numeric']
        ]
    
    def recommend_overall(self, budget, top_n=5):
        """Recommend best overall phones based on all factors"""
        filtered = self.filter_by_budget(budget)
        if len(filtered) == 0:
            return None
        
        # Normalize each feature to 0-100 scale
        filtered['camera_score'] = self.normalize(filtered['camera_mp'])
        filtered['ram_score'] = self.normalize(filtered['ram_gb'])
        filtered['battery_score'] = self.normalize(filtered['battery_mah'])
        filtered['processor_norm'] = self.normalize(filtered['processor_score'])
        filtered['rating_score'] = self.normalize(filtered['rating_numeric'].fillna(0))
        filtered['display_score'] = self.normalize(filtered['display_inches'])
        
        # Weighted overall score
        filtered['overall_score'] = (
            filtered['camera_score'] * 0.20 +
            filtered['processor_norm'] * 0.25 +
            filtered['ram_score'] * 0.15 +
            filtered['battery_score'] * 0.15 +
            filtered['rating_score'] * 0.15 +
            filtered['display_score'] * 0.10
        )
        
        return filtered.nlargest(top_n, 'overall_score')[
            ['model', 'price', 'rating', 'processor', 'camera', 'ram', 
             'battery', 'display', 'overall_score', 'price_numeric']
        ]
    
    def normalize(self, series):
        """Normalize a series to 0-100 scale"""
        if series.max() == series.min():
            return series * 0
        return (series - series.min()) / (series.max() - series.min()) * 100
    
    def display_recommendations(self, recommendations, recommendation_type):
        """Display recommendations in a formatted way"""
        if recommendations is None or len(recommendations) == 0:
            print(f"\n❌ No phones found within your budget for {recommendation_type}!")
            print("Try increasing your budget or choosing a different option.\n")
            return
        
        print(f"\n{'='*80}")
        print(f"🏆 TOP {len(recommendations)} RECOMMENDED PHONES - {recommendation_type.upper()}")
        print(f"{'='*80}\n")
        
        for idx, (_, phone) in enumerate(recommendations.iterrows(), 1):
            print(f"#{idx}. {phone['model']}")
            print(f"    💰 Price: {phone['price']}")
            if 'rating' in phone and pd.notna(phone['rating']):
                print(f"    ⭐ Rating: {phone['rating']}")
            if 'processor' in phone:
                print(f"    🔧 Processor: {phone['processor']}")
            if 'camera' in phone:
                print(f"    📷 Camera: {phone['camera']}")
            if 'ram' in phone:
                print(f"    💾 RAM: {phone['ram']}")
            if 'battery' in phone:
                print(f"    🔋 Battery: {phone['battery']}")
            if 'display' in phone:
                print(f"    📱 Display: {phone['display']}")
            if 'overall_score' in phone:
                print(f"    📊 Overall Score: {phone['overall_score']:.2f}/100")
            print()
        
        print(f"{'='*80}\n")


def main():
    """Main function to run the recommendation system"""
    print("\n" + "="*80)
    print("📱 MOBILE PHONE RECOMMENDATION SYSTEM 📱")
    print("="*80 + "\n")
    
    try:
        # Initialize the recommendation system
        recommender = PhoneRecommendationSystem()
        
        while True:
            # Get user budget
            print("💵 Enter your budget (in ₹):")
            try:
                budget = int(input("   Budget: ₹"))
                if budget <= 0:
                    print("❌ Please enter a valid budget!\n")
                    continue
            except ValueError:
                print("❌ Please enter a valid number!\n")
                continue
            
            # Show recommendation options
            print("\n🎯 Choose recommendation criteria:")
            print("   1. Camera Quality")
            print("   2. Processor Performance")
            print("   3. RAM Capacity")
            print("   4. Battery Life")
            print("   5. User Rating")
            print("   6. Overall Best (All factors)")
            print("   7. Exit")
            
            try:
                choice = int(input("\n   Enter your choice (1-7): "))
            except ValueError:
                print("❌ Please enter a valid number!\n")
                continue
            
            if choice == 7:
                print("\n👋 Thank you for using Phone Recommendation System!")
                print("="*80 + "\n")
                break
            
            # Get number of recommendations
            try:
                top_n = int(input("\n   How many recommendations? (default 5): ") or "5")
                if top_n <= 0:
                    top_n = 5
            except ValueError:
                top_n = 5
            
            # Generate recommendations based on choice
            if choice == 1:
                results = recommender.recommend_by_camera(budget, top_n)
                recommender.display_recommendations(results, "Best Camera")
            elif choice == 2:
                results = recommender.recommend_by_processor(budget, top_n)
                recommender.display_recommendations(results, "Best Processor")
            elif choice == 3:
                results = recommender.recommend_by_ram(budget, top_n)
                recommender.display_recommendations(results, "Best RAM")
            elif choice == 4:
                results = recommender.recommend_by_battery(budget, top_n)
                recommender.display_recommendations(results, "Best Battery")
            elif choice == 5:
                results = recommender.recommend_by_rating(budget, top_n)
                recommender.display_recommendations(results, "Highest Rated")
            elif choice == 6:
                results = recommender.recommend_by_overall(budget, top_n)
                recommender.display_recommendations(results, "Overall Best")
            else:
                print("❌ Invalid choice! Please choose 1-7.\n")
                continue
            
            # Ask if user wants another recommendation
            another = input("Would you like another recommendation? (y/n): ").lower()
            if another != 'y':
                print("\n👋 Thank you for using Phone Recommendation System!")
                print("="*80 + "\n")
                break
            print("\n")
    
    except FileNotFoundError:
        print("❌ Error: Could not find 'smartprix_phones_data.csv'")
        print("   Please run the smartprix-phones.ipynb notebook first to generate the data.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")


if __name__ == "__main__":
    main()
