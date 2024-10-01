# noqa: F401
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from conftest import User
from listings.models import Category, Listing


class TestReviewViews:
    @pytest.mark.django_db
    def test_create_review(self, user_fixture, listing_fixture):
        client = APIClient()
        review_url = reverse("review-list")

        # Review with valid data
        review_data = {
            "user": user_fixture.id,
            "listing": listing_fixture.id,
            "rating": 3,
            "comment": "Test Review",
        }

        # Try to post a review without authentication
        assert (
            client.post(review_url, data=review_data).status_code
            == status.HTTP_401_UNAUTHORIZED
        )

        # Authenticate the user
        client.force_authenticate(user_fixture)

        # Post a review with valid data
        response = client.post(review_url, data=review_data)
        assert response.status_code == status.HTTP_201_CREATED

        review_data["rating"] = 6
        response = client.post(review_url, data=review_data)

        # Try to post a review with invalid data
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Try to post a review on own listing
        listing = Listing.objects.create(
            title="Test Listing",
            image="listing_images/test.jpg",
            description="Test Description",
            price=100.00,
            quantity=10,
            owner_id=user_fixture.id,
            category=Category.objects.create(name="Test Category"),
        )
        # Update the review data to post a review on the listing
        review_data["listing"] = listing.id
        review_data["rating"] = 3

        response = client.post(review_url, data=review_data)

        # Check if the response is 403 Forbidden
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_retrieve_reviews(self):
        client = APIClient()
        review_url = reverse("review-list")

        # List reviews
        response = client.get(review_url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_update_review(self, user_fixture, listing_fixture):
        client = APIClient()
        client.force_authenticate(user_fixture)

        # Create a review
        review_url = reverse("review-list")
        review_data = {
            "user": user_fixture.id,
            "listing": listing_fixture.id,
            "rating": 3,
            "comment": "Test Review",
        }
        response = client.post(review_url, data=review_data)

        # Update the review
        review = response.data
        review_data["rating"] = 5
        response = client.put(f'{review_url}{review["id"]}/', data=review_data)
        assert response.status_code == status.HTTP_200_OK

        # Update the review with invalid data
        review_data["rating"] = 6
        response = client.put(f'{review_url}{review["id"]}/', data=review_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Update the review on own listing
        review_data["user"] = 1
        response = client.put(f'{review_url}{review["id"]}/', data=review_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Update the review without authentication
        client.logout()
        response = client.put(f'{review_url}{review["id"]}/', data=review_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_destroy_review(self, user_fixture, listing_fixture):
        client = APIClient()

        # Create user
        user = User.objects.create_user(
            email="second@second.com", password="password123"
        )

        # Authenticate the user
        client.force_authenticate(user)

        # Create a review
        review_url = reverse("review-list")
        review_data = {
            "user": user.id,
            "listing": listing_fixture.id,
            "rating": 3,
            "comment": "Test Review",
        }
        response = client.post(review_url, data=review_data)

        # Delete the review
        review = response.data
        response = client.delete(f'{review_url}{review["id"]}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Delete the review without authentication
        client.logout()
        response = client.delete(f'{review_url}{review["id"]}/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Delete the review on own listing with different user
        client.force_authenticate(user_fixture)
        review_data["user"] = Listing.objects.get(id=review["listing"]).owner_id
        response = client.post(review_url, data=review_data)
        review = response.data
        response = client.delete(f'{review_url}{review["id"]}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
