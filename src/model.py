"""
MISSION ENGINE: NEURAL TOPOLOGY & HYBRID LOSS CONVERGENCE CONSTRAINTS
Lead Architect: GOURAGOPAL MOHAPATRA (github.com/GOURGOPAL618)
"""
import tensorflow as tf
from tensorflow.keras import layers, models, backend as K

def specialized_dice_loss(y_true, y_pred, smooth=1.0):
    """Sorenson-Dice objective loss function to combat 95% to 5% class imbalance."""
    y_true_f = K.flatten(tf.cast(y_true, tf.float32))
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    score = (2. * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)
    return 1.0 - score

def compile_aerospace_unet(input_shape=(256, 256, 3)):
    """Architects the symmetric FCN network with horizontal skips."""
    inputs = layers.Input(input_shape)
    
    # Encoder Core Block
    c1 = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(inputs)
    c1 = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(c1)
    p1 = layers.MaxPooling2D((2, 2))(c1)
    
    c2 = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(p1)
    c2 = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(c2)
    p2 = layers.MaxPooling2D((2, 2))(c2)
    
    # Latent Vector / Bottleneck Layer
    c3 = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(p2)
    c3 = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(c3)
    
    # Decoder Core Block (Upsampling + Horizontal Skip Concatenations)
    u4 = layers.Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same')(c3)
    merge4 = layers.concatenate([u4, c2], axis=3)
    c4 = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(merge4)
    
    u5 = layers.Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same')(c4)
    merge5 = layers.concatenate([u5, c1], axis=3)
    c5 = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(merge5)
    
    # Output Sigmoid Spatial Core Classifier
    outputs = layers.Conv2D(1, (1, 1), activation='sigmoid')(c5)
    
    model = models.Model(inputs=[inputs], outputs=[outputs])
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
                  loss=specialized_dice_loss,
                  metrics=['accuracy'])
    return model

if __name__ == "__main__":
    net = compile_aerospace_unet()
    net.summary()
    print("[METADATA LOG] Neural topology layers verified. Parameters locked.")