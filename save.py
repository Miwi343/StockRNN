import numpy as np
import matplotlib as plt
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
import datetime as dt

# print( np.__version__ ) 

from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
print(tf.__version__)
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, LSTM

# Load Data
company = 'AAPL'

start = dt.datetime(2012,1,1)   #specify start and end of data reading
end = dt.datetime(2020,1,1)

data = web.DataReader(company, 'yahoo', start, end) #read in data from yahoo finances

# Prepare Data
scaler = MinMaxScaler(feature_range=(0,1))  #squeeze all prices into range from 0 to 1
scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1,1))

prediction_days = 60    #number of days in the past to use to predict future performance

x_train = []    #training data
y_train = []

for x in range(prediction_days, len(scaled_data)):  #iterate over to prepare training model 
    x_train.append(scaled_data[x-prediction_days:x, 0]) #iterate trains of length 60
    y_train.append(scaled_data[x, 0])

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))  #reshaping trains

# Build the Model
# model = Sequential()    #Recurrent Neural Network (sequential)

# model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1],1))) #1)number of layers - experimental, 2)feeds information back layers, not just forward
# model.add(Dropout(0.2))
# model.add(LSTM(units=50, return_sequences=True))
# model.add(Dropout(0.2))
# model.add(LSTM(units=50))
# model.add(Dropout(0.2))
# model.add(Dense(units=1))    #Prediction of next closing value

# model.compile(optimizer='adam', loss='mean_squared_error')  #optimizer and loss
# model.fit(x_train, y_train, epochs=25, batch_size=32)

# model.save('lstm_model.h5')
#Test the Model Accuracy on Existing Data

#Load Test Data

model = load_model('lstm_model.h5')
test_start = dt.datetime(2021,1,1)
test_end = dt.datetime.now()

test_data = web.DataReader(company, 'yahoo', test_start, test_end)
actual_prices = test_data['Close'].values

total_dataset = pd.concat((data['Close'], test_data['Close']), axis=0)

model_inputs = total_dataset[len(total_dataset) - len(test_data) - prediction_days:].values
model_inputs = model_inputs.reshape(-1, 1)
model_inputs = scaler.transform(model_inputs)

#Make Predictions on Test Data

x_test = []

for x in range(prediction_days, len(model_inputs)):
    x_test.append(model_inputs[x-prediction_days:x, 0])

x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

predicted_prices = model.predict(x_test)
predicted_prices = scaler.inverse_transform(predicted_prices)

#Plot the Test Predictions
plt.plot(actual_prices, color="black", label=f"Actual {company} Price")
plt.plot(predicted_prices, color="green", label = f"Predicted {company} Price")
plt.title(f"{company} Share Price over Time")
plt.xlabel('Time')
plt.ylabel(f"{company} Share Price")
plt.legend()
plt.show()

# Predict Next Day


real_data = [model_inputs[len(model_inputs) + 1 - prediction_days:len(model_inputs+1), 0]]
real_data = np.array(real_data)
real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1], 1))


prediction = model.predict(real_data)
prediction = scaler.inverse_transform(prediction)
print(f"Prediction: {prediction}")
