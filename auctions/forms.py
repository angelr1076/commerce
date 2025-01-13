from django.contrib.auth.models import AbstractUser
from django.forms import ModelForm
from django import forms
from .models import AbstractUser, Bid, Comment, Listing


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ('listing_title', 'listing_description',
                  'listing_img', 'category', 'closed_auction')
        ordering = ['-id']
        labels = {'listing_title': ('Item Name'), 'listing_description': ('Seller Note'), 'listing_img': (
            'Image URL'), 'closed_auction': ('Closed Auction?')}

        widgets = {
            'listing_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Think of a name that sells your product.'}),
            'listing_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tell potential bidders more about this item...'}),
            'listing_img': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'https://cutebunnyrabbits.jpg'}),
            'category': forms.Select(attrs={'class': 'form-control text-capitalize'}),
            'closed_auction': forms.HiddenInput(attrs={'class': 'form-control'}),
        }


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ('bid_amount',)
        labels = {'bid_amount': ('Your Bid')}

        widgets = {
            'bid_amount': forms.NumberInput(attrs={'step': 00.50, 'class': 'form-control', 'style': 'width:50%', 'min': 0, 'title': '', 'placeholder': ''})
        }


class CloseForm(ModelForm):
    class Meta:
        model = Listing
        fields = ('closed_auction',)
        labels = {'closed_auction': ('Close Auction?')}

        widgets = {
            'closed_auction': forms.Select(attrs={'class': 'form-control'})
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        labels = {'content': (''), }

        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control w-75', 'style': 'width:75%', 'placeholder': 'Add a comment about this item...'}),
        }
