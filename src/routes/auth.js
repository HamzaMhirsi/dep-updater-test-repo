const express = require('express');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const axios = require('axios');
const router = express.Router();

// Login endpoint
router.post('/login', async (req, res) => {
    const { email, password } = req.body;

    try {
        // Validate with external auth service
        const response = await axios.post(`${process.env.AUTH_SERVICE_URL}/validate`, {
            email,
            password,
        });

        const user = response.data;
        const isMatch = await bcrypt.compare(password, user.passwordHash);

        if (!isMatch) {
            return res.status(401).json({ error: 'Invalid credentials' });
        }

        const token = jwt.sign(
            { userId: user.id, email: user.email },
            process.env.JWT_SECRET,
            { expiresIn: '24h' }
        );

        res.json({ token, user: { id: user.id, email: user.email, name: user.name } });
    } catch (error) {
        console.error('Login error:', error.message);
        res.status(500).json({ error: 'Authentication failed' });
    }
});

// Register endpoint
router.post('/register', async (req, res) => {
    const { email, password, name } = req.body;

    try {
        const salt = await bcrypt.genSalt(10);
        const hashedPassword = await bcrypt.hash(password, salt);

        const response = await axios.post(`${process.env.AUTH_SERVICE_URL}/users`, {
            email,
            passwordHash: hashedPassword,
            name,
        });

        const token = jwt.sign(
            { userId: response.data.id, email },
            process.env.JWT_SECRET,
            { expiresIn: '24h' }
        );

        res.status(201).json({ token, user: response.data });
    } catch (error) {
        console.error('Registration error:', error.message);
        res.status(500).json({ error: 'Registration failed' });
    }
});

module.exports = router;
