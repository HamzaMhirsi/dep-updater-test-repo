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

// GDPR Art. 16 — Right to Rectification
// Allows the authenticated user to correct their own personal data.
// Updates are propagated to BOTH the user service and the auth service
// so that no data source retains stale/inaccurate personal data.
const jwt = require('jsonwebtoken');

function requireAuth(req, res, next) {
    const header = req.headers.authorization || '';
    const token = header.startsWith('Bearer ') ? header.slice(7) : null;
    if (!token) return res.status(401).json({ error: 'Unauthorized' });
    try {
        req.user = jwt.verify(token, process.env.JWT_SECRET);
        next();
    } catch (e) {
        return res.status(401).json({ error: 'Invalid token' });
    }
}

// Whitelist of fields a data subject is allowed to rectify about themselves.
const RECTIFIABLE_FIELDS = ['name', 'email', 'phone', 'address', 'locale'];

router.patch('/me', requireAuth, async (req, res) => {
    const userId = req.user.userId;
    const updates = _.pick(req.body || {}, RECTIFIABLE_FIELDS);

    if (_.isEmpty(updates)) {
        return res.status(400).json({ error: 'No rectifiable fields provided' });
    }

    try {
        // 1. Update primary user store
        const userResp = await axios.patch(
            `${process.env.USER_SERVICE_URL}/users/${userId}`,
            updates
        );

        // 2. Propagate identity-affecting fields to the auth service
        //    so that login/identity records are not left inaccurate.
        if (updates.email) {
            await axios.patch(
                `${process.env.AUTH_SERVICE_URL}/users/${userId}`,
                { email: updates.email }
            );
        }

        // 3. Audit log the rectification (GDPR accountability — Art. 5(2))
        console.log(JSON.stringify({
            event: 'gdpr.rectification',
            article: 'Art.16',
            userId,
            fields: Object.keys(updates),
            timestamp: new Date().toISOString(),
        }));

        const safe = _.omit(userResp.data, ['passwordHash', 'internalId']);
        res.json(safe);
    } catch (error) {
        console.error('Rectification error:', error.message);
        res.status(500).json({ error: 'Failed to update profile' });
    }
});
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
