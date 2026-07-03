# Deployment Checklist

## Pre-Deployment
- [ ] Set DEBUG=False in settings.py
- [ ] Update ALLOWED_HOSTS with your domain
- [ ] Set SECRET_KEY using environment variable
- [ ] Configure database for production
- [ ] Collect static files: python manage.py collectstatic

## Environment Variables
- SECRET_KEY
- DATABASE_URL
- OPENAI_API_KEY or GEMINI_API_KEY

## Post-Deployment
- [ ] Test all features
- [ ] Check error pages
- [ ] Verify database backups
- [ ] Monitor performance
- [ ] Set up SSL certificate