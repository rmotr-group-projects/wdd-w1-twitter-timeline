# Twitter Clone

This is the firs project of our [Web Development with Django course](https://rmotr.com/web-development-with-django). It's just a simple twitter clone implemented with Django. One of the main objectives of this project is to bring you up to speed with the process of working with Github and the first Django setup. Also, you'll see the power of Django as you'll be able to build a simple twitter clone in a few hours.

## Description of the project

This project counts with a few Django features: authentication, forms, models, templates and statics. Tests are located in the `test_twitter_clone.py` (you can see how to run them below) file. Here's a description of the site with screenshots.

### Not authenticated pages

Pages and how they look for a not authenticated user (anonymous).

#### Login page

The home page (`'/'`) is only for authenticated users

![image](https://cloud.githubusercontent.com/assets/872296/17901146/8b9b27be-6938-11e6-8b7f-3b03dc6065fa.png)

#### Empty user's profile

![image](https://cloud.githubusercontent.com/assets/872296/17901227/dd1947e2-6938-11e6-89f2-7b6058ce83f7.png)

#### Profile with tweets

![image](https://cloud.githubusercontent.com/assets/872296/17901272/0e5a9b62-6939-11e6-9dc4-6c6f88fc1d62.png)

### Authenticated Pages

If the user is authenticated she/he should see:

### Home

![image](https://cloud.githubusercontent.com/assets/872296/17901320/411661e4-6939-11e6-8222-ccb12062b4ca.png)
_(Note the form to compose a tweet and the delete icons to delete tweets)_

### Post a tweet successfully

![image](https://cloud.githubusercontent.com/assets/872296/17901393/95ac5ea2-6939-11e6-920d-734261dcf252.png)


### Posting a tweet with more than 140 chars

![image](https://cloud.githubusercontent.com/assets/872296/17901520/1f5ef5f6-693a-11e6-89b6-30fd5610790e.png)

### Deleting a tweet

![image](https://cloud.githubusercontent.com/assets/872296/17901533/36b92212-693a-11e6-9141-9e2f52048011.png)
