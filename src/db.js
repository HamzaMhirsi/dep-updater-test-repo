const mongoose = require('mongoose');

// Deprecated options: useNewUrlParser, useUnifiedTopology, useCreateIndex, useFindAndModify
// were removed in mongoose 8.x
async function connectDB() {
    try {
        mongoose.set('useCreateIndex', true);
        mongoose.set('useFindAndModify', false);

        await mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/testapp', {
            useNewUrlParser: true,
            useUnifiedTopology: true,
            poolSize: 10,
            bufferMaxEntries: 0,
        });
        console.log('MongoDB connected');
    } catch (error) {
        console.error('MongoDB connection error:', error.message);
        process.exit(1);
    }
}

// Deprecated: mongoose.connection.once() pattern
mongoose.connection.once('open', () => {
    console.log('MongoDB connection is open');
});

module.exports = { connectDB };
