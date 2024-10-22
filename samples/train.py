import tensorflow as tf
from object_detection.utils import dataset_util

# Load your dataset
train_images, train_labels = load_dataset('train')
val_images, val_labels = load_dataset('val')

# Convert your dataset to TFRecords
train_tfrecords = dataset_util.tf_record_creation_util.create_tf_record('train', train_images, train_labels)
val_tfrecords = dataset_util.tf_record_creation_util.create_tf_record('val', val_images, val_labels)

# Load a pre-trained model
model = tf.keras.applications.EfficientDetD0(weights='imagenet')

# Replace the last layer for transfer learning
model.layers[-1] = tf.keras.layers.Dense(2, activation='softmax')

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(train_tfrecords, validation_data=val_tfrecords, epochs=10)

# Save the model
model.save('strawberry_model.h5')