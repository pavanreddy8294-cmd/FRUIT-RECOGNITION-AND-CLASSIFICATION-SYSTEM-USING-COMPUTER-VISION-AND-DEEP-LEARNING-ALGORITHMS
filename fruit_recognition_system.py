"""
Fruit Recognition and Classification System
Uses Computer Vision and Deep Learning to identify and classify fruits
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image, ImageDraw, ImageFont
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
import warnings
warnings.filterwarnings('ignore')

# Set style for visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

def create_synthetic_fruit_images(n_images=500, fruit_types=['Apple', 'Banana', 'Orange', 'Mango', 'Strawberry']):
    """Create synthetic fruit images with color features"""
    np.random.seed(42)
    
    image_data = []
    labels = []
    
    fruit_colors = {
        'Apple': {'r': (200, 255), 'g': (50, 150), 'b': (50, 150)},
        'Banana': {'r': (200, 255), 'g': (200, 255), 'b': (0, 100)},
        'Orange': {'r': (200, 255), 'g': (100, 200), 'b': (0, 100)},
        'Mango': {'r': (180, 255), 'g': (100, 200), 'b': (0, 100)},
        'Strawberry': {'r': (200, 255), 'g': (50, 150), 'b': (50, 150)}
    }
    
    for fruit_type in fruit_types:
        for i in range(n_images // len(fruit_types)):
            # Create synthetic image
            img = Image.new('RGB', (64, 64), color=(255, 255, 255))
            pixels = img.load()
            
            # Get fruit color ranges
            color_range = fruit_colors[fruit_type]
            
            # Generate fruit-like image with color variations
            for x in range(64):
                for y in range(64):
                    # Create circular fruit shape
                    dist_from_center = np.sqrt((x - 32)**2 + (y - 32)**2)
                    
                    if dist_from_center < 25:
                        r = np.random.randint(color_range['r'][0], color_range['r'][1])
                        g = np.random.randint(color_range['g'][0], color_range['g'][1])
                        b = np.random.randint(color_range['b'][0], color_range['b'][1])
                        
                        # Add texture variation
                        r = max(0, min(255, r + np.random.randint(-20, 20)))
                        g = max(0, min(255, g + np.random.randint(-20, 20)))
                        b = max(0, min(255, b + np.random.randint(-20, 20)))
                        
                        pixels[x, y] = (r, g, b)
            
            # Extract features from image
            img_array = np.array(img)
            features = extract_image_features(img_array)
            image_data.append(features)
            labels.append(fruit_type)
    
    return np.array(image_data), np.array(labels)

def extract_image_features(img_array):
    """Extract color and texture features from image"""
    # Reshape if needed
    if len(img_array.shape) == 3:
        # RGB image
        r_channel = img_array[:, :, 0].flatten()
        g_channel = img_array[:, :, 1].flatten()
        b_channel = img_array[:, :, 2].flatten()
        
        features = [
            np.mean(r_channel), np.std(r_channel),
            np.mean(g_channel), np.std(g_channel),
            np.mean(b_channel), np.std(b_channel),
            np.mean(r_channel) - np.mean(b_channel),  # Red-Blue ratio
            np.mean(g_channel) - np.mean(r_channel),  # Green-Red ratio
            np.max(r_channel) - np.min(r_channel),    # R range
            np.max(g_channel) - np.min(g_channel),    # G range
            np.max(b_channel) - np.min(b_channel),    # B range
            np.mean([np.mean(r_channel), np.mean(g_channel), np.mean(b_channel)])  # Brightness
        ]
    else:
        features = [0] * 12
    
    return np.array(features)

def train_models(X_train, X_test, y_train, y_test):
    """Train multiple classification models"""
    models = {}
    results = {}
    
    # Model 1: Random Forest (Simulating CNN-like feature extraction)
    print("Training Random Forest Classifier...")
    rf_model = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    y_pred_proba_rf = rf_model.predict_proba(X_test)
    
    models['Random Forest'] = rf_model
    results['Random Forest'] = {
        'predictions': y_pred_rf,
        'probabilities': y_pred_proba_rf,
        'accuracy': accuracy_score(y_test, y_pred_rf),
        'precision': precision_score(y_test, y_pred_rf, average='weighted', zero_division=0),
        'recall': recall_score(y_test, y_pred_rf, average='weighted', zero_division=0),
        'f1': f1_score(y_test, y_pred_rf, average='weighted', zero_division=0)
    }
    
    # Model 2: Support Vector Machine
    print("Training Support Vector Machine...")
    svm_model = SVC(kernel='rbf', C=1.0, gamma='scale', probability=True, random_state=42)
    svm_model.fit(X_train, y_train)
    y_pred_svm = svm_model.predict(X_test)
    y_pred_proba_svm = svm_model.predict_proba(X_test)
    
    models['SVM'] = svm_model
    results['SVM'] = {
        'predictions': y_pred_svm,
        'probabilities': y_pred_proba_svm,
        'accuracy': accuracy_score(y_test, y_pred_svm),
        'precision': precision_score(y_test, y_pred_svm, average='weighted', zero_division=0),
        'recall': recall_score(y_test, y_pred_svm, average='weighted', zero_division=0),
        'f1': f1_score(y_test, y_pred_svm, average='weighted', zero_division=0)
    }
    
    # Model 3: Neural Network (MLP - simulating deep learning)
    print("Training Neural Network (MLP)...")
    nn_model = MLPClassifier(hidden_layer_sizes=(128, 64, 32), max_iter=500, random_state=42)
    nn_model.fit(X_train, y_train)
    y_pred_nn = nn_model.predict(X_test)
    y_pred_proba_nn = nn_model.predict_proba(X_test)
    
    models['Neural Network'] = nn_model
    results['Neural Network'] = {
        'predictions': y_pred_nn,
        'probabilities': y_pred_proba_nn,
        'accuracy': accuracy_score(y_test, y_pred_nn),
        'precision': precision_score(y_test, y_pred_nn, average='weighted', zero_division=0),
        'recall': recall_score(y_test, y_pred_nn, average='weighted', zero_division=0),
        'f1': f1_score(y_test, y_pred_nn, average='weighted', zero_division=0)
    }
    
    return models, results

def plot_fruit_distribution(labels):
    """Plot distribution of fruit types"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    unique, counts = np.unique(labels, return_counts=True)
    colors = ['#FF6B6B', '#FFE66D', '#FF9F1C', '#FFBE0B', '#FB5607']
    
    axes[0].bar(unique, counts, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[0].set_ylabel('Count', fontsize=11, fontweight='bold')
    axes[0].set_title('Distribution of Fruit Types in Dataset', fontsize=12, fontweight='bold')
    axes[0].grid(axis='y', alpha=0.3)
    for i, v in enumerate(counts):
        axes[0].text(i, v + 2, str(v), ha='center', fontweight='bold')
    
    axes[1].pie(counts, labels=unique, colors=colors, autopct='%1.1f%%', startangle=90,
               textprops={'fontsize': 11, 'fontweight': 'bold'})
    axes[1].set_title('Fruit Type Distribution', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/fruit_distribution.png', dpi=300, bbox_inches='tight')
    print("Saved: fruit_distribution.png")
    plt.close()

def plot_model_comparison(results):
    """Compare model performance metrics"""
    models = list(results.keys())
    metrics = ['accuracy', 'precision', 'recall', 'f1']
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    colors = ['#3498db', '#e74c3c', '#f39c12']
    
    for idx, metric in enumerate(metrics):
        values = [results[m][metric] for m in models]
        axes[idx].bar(models, values, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
        axes[idx].set_ylabel(metric.upper(), fontsize=11, fontweight='bold')
        axes[idx].set_title(f'{metric.upper()} Comparison', fontsize=12, fontweight='bold')
        axes[idx].set_ylim([0, 1])
        axes[idx].grid(axis='y', alpha=0.3)
        for i, v in enumerate(values):
            axes[idx].text(i, v + 0.02, f'{v:.4f}', ha='center', fontweight='bold', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/fruit_model_comparison.png', dpi=300, bbox_inches='tight')
    print("Saved: fruit_model_comparison.png")
    plt.close()

def plot_confusion_matrices(results, y_test, fruit_types):
    """Plot confusion matrices for all models"""
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    for idx, (model_name, result) in enumerate(results.items()):
        cm = confusion_matrix(y_test, result['predictions'], labels=fruit_types)
        
        sns.heatmap(cm, annot=True, fmt='d', cmap='YlOrRd', ax=axes[idx],
                   cbar=False, annot_kws={'fontsize': 10, 'fontweight': 'bold'},
                   xticklabels=fruit_types, yticklabels=fruit_types)
        axes[idx].set_xlabel('Predicted', fontsize=11, fontweight='bold')
        axes[idx].set_ylabel('Actual', fontsize=11, fontweight='bold')
        axes[idx].set_title(f'{model_name}\nAccuracy: {result["accuracy"]:.4f}', 
                           fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/fruit_confusion_matrices.png', dpi=300, bbox_inches='tight')
    print("Saved: fruit_confusion_matrices.png")
    plt.close()

def plot_feature_importance(models, feature_names):
    """Plot feature importance for tree-based models"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Random Forest
    rf_importance = models['Random Forest'].feature_importances_
    rf_indices = np.argsort(rf_importance)[-10:]
    axes[0].barh(range(len(rf_indices)), rf_importance[rf_indices], 
                color='#3498db', alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[0].set_yticks(range(len(rf_indices)))
    axes[0].set_yticklabels([feature_names[i] for i in rf_indices], fontsize=10)
    axes[0].set_xlabel('Importance', fontsize=11, fontweight='bold')
    axes[0].set_title('Random Forest - Feature Importance', fontsize=12, fontweight='bold')
    axes[0].grid(axis='x', alpha=0.3)
    
    # Neural Network weights visualization
    nn_model = models['Neural Network']
    first_layer_weights = np.abs(nn_model.coefs_[0])
    feature_importance_nn = np.mean(first_layer_weights, axis=1)
    nn_indices = np.argsort(feature_importance_nn)[-10:]
    
    axes[1].barh(range(len(nn_indices)), feature_importance_nn[nn_indices], 
                color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[1].set_yticks(range(len(nn_indices)))
    axes[1].set_yticklabels([feature_names[i] for i in nn_indices], fontsize=10)
    axes[1].set_xlabel('Importance', fontsize=11, fontweight='bold')
    axes[1].set_title('Neural Network - Feature Importance', fontsize=12, fontweight='bold')
    axes[1].grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/fruit_feature_importance.png', dpi=300, bbox_inches='tight')
    print("Saved: fruit_feature_importance.png")
    plt.close()

def plot_color_distribution(X_data, labels, fruit_types):
    """Plot color feature distribution by fruit type"""
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    axes = axes.flatten()
    
    colors_map = ['#FF6B6B', '#FFE66D', '#FF9F1C', '#FFBE0B', '#FB5607']
    
    for idx, fruit_type in enumerate(fruit_types):
        fruit_mask = labels == fruit_type
        fruit_data = X_data[fruit_mask]
        
        # Plot RGB means
        r_means = fruit_data[:, 0]
        g_means = fruit_data[:, 1]
        b_means = fruit_data[:, 2]
        
        axes[idx].scatter(r_means, g_means, c=colors_map[idx], s=50, alpha=0.6, 
                         edgecolors='black', linewidth=0.5, label='R vs G')
        axes[idx].set_xlabel('Red Channel Mean', fontsize=10, fontweight='bold')
        axes[idx].set_ylabel('Green Channel Mean', fontsize=10, fontweight='bold')
        axes[idx].set_title(f'{fruit_type} - Color Distribution', fontsize=11, fontweight='bold')
        axes[idx].grid(alpha=0.3)
    
    # Remove extra subplot
    fig.delaxes(axes[5])
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/fruit_color_distribution.png', dpi=300, bbox_inches='tight')
    print("Saved: fruit_color_distribution.png")
    plt.close()

def plot_prediction_confidence(results, y_test, fruit_types):
    """Plot prediction confidence distribution"""
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    for idx, (model_name, result) in enumerate(results.items()):
        max_proba = np.max(result['probabilities'], axis=1)
        
        axes[idx].hist(max_proba, bins=20, color=['#3498db', '#e74c3c', '#f39c12'][idx], 
                      alpha=0.7, edgecolor='black', linewidth=1.5)
        axes[idx].set_xlabel('Prediction Confidence', fontsize=11, fontweight='bold')
        axes[idx].set_ylabel('Frequency', fontsize=11, fontweight='bold')
        axes[idx].set_title(f'{model_name} - Prediction Confidence', fontsize=12, fontweight='bold')
        axes[idx].axvline(np.mean(max_proba), color='red', linestyle='--', linewidth=2, label=f'Mean: {np.mean(max_proba):.3f}')
        axes[idx].legend()
        axes[idx].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/fruit_prediction_confidence.png', dpi=300, bbox_inches='tight')
    print("Saved: fruit_prediction_confidence.png")
    plt.close()

def main():
    print("="*80)
    print("FRUIT RECOGNITION AND CLASSIFICATION SYSTEM - DEEP LEARNING ANALYSIS")
    print("="*80)
    
    fruit_types = ['Apple', 'Banana', 'Orange', 'Mango', 'Strawberry']
    
    # Generate synthetic dataset
    print("\n[1] Generating synthetic fruit image dataset...")
    X, y = create_synthetic_fruit_images(n_images=500, fruit_types=fruit_types)
    print(f"Dataset generated: {X.shape[0]} images, {X.shape[1]} features")
    print(f"Fruit types: {fruit_types}")
    for fruit in fruit_types:
        count = np.sum(y == fruit)
        print(f"  {fruit}: {count} images")
    
    # Prepare data
    print("\n[2] Preparing and preprocessing data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"Training set: {X_train_scaled.shape[0]} samples")
    print(f"Test set: {X_test_scaled.shape[0]} samples")
    
    # Train models
    print("\n[3] Training classification models...")
    models, results = train_models(X_train_scaled, X_test_scaled, y_train, y_test)
    
    # Print results
    print("\n[4] Model Performance Results:")
    print("-" * 80)
    for model_name, result in results.items():
        print(f"\n{model_name}:")
        print(f"  Accuracy:  {result['accuracy']:.6f}")
        print(f"  Precision: {result['precision']:.6f}")
        print(f"  Recall:    {result['recall']:.6f}")
        print(f"  F1-Score:  {result['f1']:.6f}")
    
    # Generate visualizations
    print("\n[5] Generating visualizations...")
    plot_fruit_distribution(y)
    plot_model_comparison(results)
    plot_confusion_matrices(results, y_test, fruit_types)
    plot_feature_importance(models, ['R_Mean', 'R_Std', 'G_Mean', 'G_Std', 'B_Mean', 'B_Std', 
                                      'R-B_Ratio', 'G-R_Ratio', 'R_Range', 'G_Range', 'B_Range', 'Brightness'])
    plot_color_distribution(X_test_scaled, y_test, fruit_types)
    plot_prediction_confidence(results, y_test, fruit_types)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE - All visualizations saved")
    print("="*80)

if __name__ == "__main__":
    main()
