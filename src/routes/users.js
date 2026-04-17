const express = require('express');
const _ = require('lodash');
const axios = require('axios');
const router = express.Router();

// Get all users
router.get('/', async (req, res) => {
    try {
        const response = await axios.get(`${process.env.USER_SERVICE_URL}/users`);
        const users = response.data;

        // Use lodash to transform and filter
        const activeUsers = _.filter(users, { isActive: true });
        const formatted = _.map(activeUsers, user => _.pick(user, ['id', 'name', 'email', 'role']));
        const sorted = _.sortBy(formatted, 'name');

        res.json(sorted);
    } catch (error) {
        console.error('Error fetching users:', error.message);
        res.status(500).json({ error: 'Failed to fetch users' });
    }
});

// Get user by ID
router.get('/:id', async (req, res) => {
    try {
        const response = await axios.get(`${process.env.USER_SERVICE_URL}/users/${req.params.id}`);
        const user = _.omit(response.data, ['passwordHash', 'internalId']);
        res.json(user);
    } catch (error) {
        res.status(404).json({ error: 'User not found' });
    }
});

// Search users
router.get('/search', async (req, res) => {
    const { query } = req.query;
    try {
        const response = await axios.get(`${process.env.USER_SERVICE_URL}/users`);
        const matches = _.filter(response.data, user =>
            _.includes(_.toLower(user.name), _.toLower(query)) ||
            _.includes(_.toLower(user.email), _.toLower(query))
        );
        res.json(matches);
    } catch (error) {
        res.status(500).json({ error: 'Search failed' });
    }
});

module.exports = router;
