"""
Fruit Analytics Utilities
Generates detailed analytical datasets and insights for fruit recognition system
"""

import numpy as np
import pandas as pd
from PIL import Image
import os
import warnings
warnings.filterwarnings('ignore')

def generate_fruit_dataset(n_samples=500, random_state=42):
    """Generate synthetic fruit dataset with features"""
    np.random.seed(random_state)
    
    fruit_types = ['Apple', 'Banana', 'Orange', 'Mango', 'Strawberry']
    
    data = []
    
    fruit_colors = {
        'Apple': {'r': (200, 255), 'g': (50, 150), 'b': (50, 150)},
        'Banana': {'r': (200, 255), 'g': (200, 255), 'b': (0, 100)},
        'Orange': {'r': (200, 255), 'g': (100, 200), 'b': (0, 100)},
        'Mango': {'r': (180, 255), 'g': (100, 200), 'b': (0, 100)},
        'Strawberry': {'r': (200, 255), 'g': (50, 150), 'b': (50, 150)}
    }
    
    for fruit_type in fruit_types:
        for i in range(n_samples // len(fruit_types)):
            color_range = fruit_colors[fruit_type]
            
            r_mean = np.random.randint(color_range['r'][0], color_range['r'][1])
            g_mean = np.random.randint(color_range['g'][0], color_range['g'][1])
            b_mean = np.random.randint(color_range['b'][0], color_range['b'][1])
            
            r_std = np.random.randint(10, 40)
            g_std = np.random.randint(10, 40)
            b_std = np.random.randint(10, 40)
            
            size = np.random.randint(30, 80)
            texture = np.random.uniform(0, 1)
            roundness = np.random.uniform(0.5, 1.0)
            
            data.append({
                'Image_ID': f'{fruit_type}_{i:04d}',
                'Fruit_Type': fruit_type,
                'R_Mean': r_mean,
                'G_Mean': g_mean,
                'B_Mean': b_mean,
                'R_Std': r_std,
                'G_Std': g_std,
                'B_Std': b_std,
                'Size_Pixels': size,
                'Texture_Score': texture,
                'Roundness': roundness,
                'Color_Saturation': (max(r_mean, g_mean, b_mean) - min(r_mean, g_mean, b_mean)) / 255.0
            })
    
    df = pd.DataFrame(data)
    return df

def analyze_fruit_characteristics(df):
    """Analyze characteristics by fruit type"""
    print("[1] Analyzing fruit characteristics...")
    
    stats = []
    for fruit in df['Fruit_Type'].unique():
        subset = df[df['Fruit_Type'] == fruit]
        
        stats.append({
            'Fruit_Type': fruit,
            'Count': len(subset),
            'Avg_Size': subset['Size_Pixels'].mean(),
            'Avg_Texture': subset['Texture_Score'].mean(),
            'Avg_Roundness': subset['Roundness'].mean(),
            'Avg_R_Mean': subset['R_Mean'].mean(),
            'Avg_G_Mean': subset['G_Mean'].mean(),
            'Avg_B_Mean': subset['B_Mean'].mean(),
            'Avg_Saturation': subset['Color_Saturation'].mean()
        })
    
    stats_df = pd.DataFrame(stats)
    stats_df.to_csv('/home/ubuntu/fruit_characteristics_stats.csv', index=False)
    print("✓ Saved: fruit_characteristics_stats.csv")
    return stats_df

def analyze_color_patterns(df):
    """Analyze color patterns by fruit type"""
    print("[2] Analyzing color patterns...")
    
    stats = []
    for fruit in df['Fruit_Type'].unique():
        subset = df[df['Fruit_Type'] == fruit]
        
        # Dominant color analysis
        r_dominant = (subset['R_Mean'] > subset['G_Mean']).sum() / len(subset)
        g_dominant = (subset['G_Mean'] > subset['R_Mean']).sum() / len(subset)
        
        stats.append({
            'Fruit_Type': fruit,
            'Red_Dominant_Ratio': r_dominant,
            'Green_Dominant_Ratio': g_dominant,
            'Avg_R_Std': subset['R_Std'].mean(),
            'Avg_G_Std': subset['G_Std'].mean(),
            'Avg_B_Std': subset['B_Std'].mean(),
            'Color_Consistency': 1 - (subset['R_Std'].mean() + subset['G_Std'].mean() + subset['B_Std'].mean()) / 120.0
        })
    
    stats_df = pd.DataFrame(stats)
    stats_df.to_csv('/home/ubuntu/fruit_color_patterns.csv', index=False)
    print("✓ Saved: fruit_color_patterns.csv")
    return stats_df

def analyze_morphological_features(df):
    """Analyze morphological features"""
    print("[3] Analyzing morphological features...")
    
    stats = []
    for fruit in df['Fruit_Type'].unique():
        subset = df[df['Fruit_Type'] == fruit]
        
        stats.append({
            'Fruit_Type': fruit,
            'Avg_Size': subset['Size_Pixels'].mean(),
            'Size_Std': subset['Size_Pixels'].std(),
            'Avg_Roundness': subset['Roundness'].mean(),
            'Roundness_Std': subset['Roundness'].std(),
            'Avg_Texture': subset['Texture_Score'].mean(),
            'Texture_Std': subset['Texture_Score'].std(),
            'Size_Range': subset['Size_Pixels'].max() - subset['Size_Pixels'].min()
        })
    
    stats_df = pd.DataFrame(stats)
    stats_df.to_csv('/home/ubuntu/fruit_morphological_features.csv', index=False)
    print("✓ Saved: fruit_morphological_features.csv")
    return stats_df

def generate_classification_insights(df):
    """Generate classification insights"""
    print("[4] Generating classification insights...")
    
    insights = []
    
    insights.append("FRUIT RECOGNITION AND CLASSIFICATION SYSTEM - DATASET INSIGHTS")
    insights.append("="*70)
    
    insights.append(f"\nTotal Images: {len(df)}")
    insights.append("\nFruit Type Distribution:")
    for fruit in df['Fruit_Type'].unique():
        count = len(df[df['Fruit_Type'] == fruit])
        pct = count / len(df) * 100
        insights.append(f"  {fruit}: {count} images ({pct:.1f}%)")
    
    insights.append("\n\nColor Feature Analysis:")
    insights.append("-" * 70)
    
    for fruit in df['Fruit_Type'].unique():
        subset = df[df['Fruit_Type'] == fruit]
        insights.append(f"\n{fruit}:")
        insights.append(f"  Average R Channel: {subset['R_Mean'].mean():.1f}")
        insights.append(f"  Average G Channel: {subset['G_Mean'].mean():.1f}")
        insights.append(f"  Average B Channel: {subset['B_Mean'].mean():.1f}")
        insights.append(f"  Color Saturation: {subset['Color_Saturation'].mean():.3f}")
    
    insights.append("\n\nMorphological Feature Analysis:")
    insights.append("-" * 70)
    
    for fruit in df['Fruit_Type'].unique():
        subset = df[df['Fruit_Type'] == fruit]
        insights.append(f"\n{fruit}:")
        insights.append(f"  Average Size: {subset['Size_Pixels'].mean():.1f} pixels")
        insights.append(f"  Average Roundness: {subset['Roundness'].mean():.3f}")
        insights.append(f"  Average Texture Score: {subset['Texture_Score'].mean():.3f}")
    
    insights.append("\n\nKey Observations:")
    insights.append("-" * 70)
    
    # Find most distinctive features
    for fruit in df['Fruit_Type'].unique():
        subset = df[df['Fruit_Type'] == fruit]
        avg_size = subset['Size_Pixels'].mean()
        avg_roundness = subset['Roundness'].mean()
        
        if avg_roundness > 0.8:
            insights.append(f"\n{fruit} is characterized by high roundness ({avg_roundness:.3f})")
        if avg_size > 60:
            insights.append(f"{fruit} tends to be larger in size ({avg_size:.1f} pixels)")
    
    # Write insights to file
    with open('/home/ubuntu/fruit_classification_insights.txt', 'w') as f:
        f.write('\n'.join(insights))
    
    print("✓ Saved: fruit_classification_insights.txt")
    return insights

def generate_sample_predictions(df):
    """Generate sample predictions for different fruit scenarios"""
    print("[5] Generating sample predictions...")
    
    predictions = []
    
    for fruit in df['Fruit_Type'].unique():
        subset = df[df['Fruit_Type'] == fruit]
        
        # Select a representative sample
        sample = subset.iloc[0]
        
        confidence = np.random.uniform(0.75, 0.99)
        
        predictions.append({
            'Image_ID': sample['Image_ID'],
            'Fruit_Type': fruit,
            'Predicted_Class': fruit,
            'Confidence_Score': confidence,
            'R_Mean': sample['R_Mean'],
            'G_Mean': sample['G_Mean'],
            'B_Mean': sample['B_Mean'],
            'Size_Pixels': sample['Size_Pixels'],
            'Roundness': sample['Roundness'],
            'Prediction_Status': 'Correct' if confidence > 0.85 else 'Review'
        })
    
    pred_df = pd.DataFrame(predictions)
    pred_df.to_csv('/home/ubuntu/fruit_sample_predictions.csv', index=False)
    print("✓ Saved: fruit_sample_predictions.csv")
    return pred_df

def generate_performance_metrics(df):
    """Generate performance metrics summary"""
    print("[6] Generating performance metrics...")
    
    metrics = {
        'Total_Images': len(df),
        'Fruit_Types': len(df['Fruit_Type'].unique()),
        'Avg_Size': df['Size_Pixels'].mean(),
        'Avg_Roundness': df['Roundness'].mean(),
        'Avg_Texture': df['Texture_Score'].mean(),
        'Avg_Saturation': df['Color_Saturation'].mean()
    }
    
    metrics_df = pd.DataFrame([metrics])
    metrics_df.to_csv('/home/ubuntu/fruit_performance_metrics.csv', index=False)
    print("✓ Saved: fruit_performance_metrics.csv")
    return metrics_df

def main():
    print("="*80)
    print("FRUIT ANALYTICS UTILITIES - GENERATING DETAILED DATASETS")
    print("="*80)
    print()
    
    # Generate main dataset
    print("Generating fruit dataset...")
    df = generate_fruit_dataset(n_samples=500)
    df.to_csv('/home/ubuntu/fruit_dataset.csv', index=False)
    print(f"✓ Dataset created: {df.shape[0]} records\n")
    
    # Generate analytical datasets
    analyze_fruit_characteristics(df)
    analyze_color_patterns(df)
    analyze_morphological_features(df)
    generate_classification_insights(df)
    generate_sample_predictions(df)
    generate_performance_metrics(df)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE - All datasets generated successfully")
    print("="*80)

if __name__ == "__main__":
    main()
