# Import some stuff to be used in the file
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from .models import *
from utilities import PaginateObjects
from threading import Thread
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging, time, datetime, os, smtplib, ssl
from django.utils import timezone
from blog.models import Post, Video


# current_path = os.path.dirname(os.path.realpath(__file__))
# current_path = os.path.dirname(os.path.abspath(__file__))
# logging.config.fileConfig(current_path+ "../logging.ini")
# logging.config.fileConfig('C:/Users/Deciphrexx/coding/python/django/Ainaproj/logging.ini')
logging.config.fileConfig(os.path.join(settings.BASE_DIR, 'logging.ini'))


# loggers that will be used in the code
activity_logger = logging.getLogger('ActivityLogger')  
stdout_logger = logging.getLogger('root')

'''
Todo: 

  - Use the messages framework to create a popup box that 
    tells the user that their message(s) has been successfully sent
    on the index and contact pages.
'''


# this is just a mixin(or parent class) that some view classes will inherit from
class MyCustomMixin(View):
    queryset1, queryset2, queryset3, queryset4, queryset5 = (None, None, None, None, None)
    form_class1, form_class2, form_class3 = (None, None, None)
    template_name = None
    footer_events = Event.objects.all().order_by('-date')[:2]

    def __init__(self):
        super(View, self).__init__()
        self.forms = {'form_1':self.form_class1, 'form_2':self.form_class2, 'form_3':self.form_class3}
        self.querysets = {'queryset_1': self.queryset1, 'queryset_2':self.queryset2, 'queryset_3':self.queryset3, 'queryset_4':self.queryset4, 'queryset_5':self.queryset5, 'footer_events':self.footer_events}
        self.context = {**self.forms, **self.querysets}
    


    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)
    
    
    def email_io_operation(self, request):
        # print(request.POST, 'THIS IS THE POST REQUEST')
        
        # This will create a volunteer object in the database
        Volunteer.objects.create(name=request.POST.get('volunteer_name'), email=request.POST.get('volunteer_email'))



        em1 = MIMEMultipart()
        em1['From'] = 'AinaAbosede Foundation'
        em1['Subject'] = f"Hi {' '.join(request.POST.get('volunteer_name').split(' ')[:2])}, thank you for your interest in volunteering with AinaAbosede Charity Foundation"
        em1.attach(MIMEText(f"""
Dear {' '.join(request.POST.get('volunteer_name').split(' ')[:2])},

Thank you for expressing your interest in volunteering with AinaAbosede Foundation. We are thrilled to have you as a potential member of our team and appreciate your willingness to give back to the community.

We have a variety of volunteer opportunities available, such as [list specific opportunities]. Before we proceed with the next steps, please take a moment to review our volunteer requirements and expectations, which can be found on our website at [insert link].

After you have reviewed the requirements, please let us know which volunteer opportunity you are most interested in and any relevant skills or experience you have that would make you a great fit for the role. We would also appreciate it if you could provide us with your current resume or CV.

Once we have received this information, we will review your application and be in touch with you shortly to schedule an interview or provide further information about the next steps in the process.

Thank you again for your interest in volunteering with AinaAbosede Charity Foundation. We look forward to working with you to make a positive impact in the community.

Best regards,
AinaAbosede Foundation team.
""", 'plain'))


        em2 = MIMEMultipart()
        em2['subject'] = f"{request.POST.get('volunteer_name')} wants to volunteer for the Foundation."
        em2.attach(MIMEText(f"""
{' '.join(request.POST.get('volunteer_name').split(' ')[:2])} filled out the volunteer form and the message was as follows:
““
{request.POST.get('volunteer_message')}
””
""", 'html'))


        stdout_logger.info("PROCESSING THE DATA...")
        with smtplib.SMTP_SSL(settings.EMAIL_SERVER, settings.EMAIL_PORT, context=ssl.create_default_context()) as smtp:
            smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            
            
            # sending an email to the volunteer.
            to_email = request.POST.get('volunteer_email') or settings.DEFAULT_TO_EMAIL
            smtp.sendmail(settings.EMAIL_HOST_USER, to_email, em1.as_string())
            activity_logger.info(f"Email sent to {request.POST.get('volunteer_name')} (volunteer).")
            
            # sending an email to the site email address.
            smtp.sendmail(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_USER, em2.as_string())
            stdout_logger.info("EMAILS SENT SUCCESSFULLY !!!")


    def post(self, request, *args, **kwargs):
        '''
        Note : My reason for designing the email operation this way is because:
        [I]  -  The post request calls on a method which can be easily overridden from the child classes
                and if it the email operations was put directly in the post method, then we would have
                to override the whole post method in the child classes!
        [II] -  I am using threading to send these mails in a separate thread from the main thread(non-daemon)
                and it just makes sense to create an external function for this to work, i.e another method 
                other that the post method.
        '''

        '''
        this gets triggered only from child classes that have send_email_messages as a
        part of the post request and it starts a thread with self.email_io_operation
        which will be created in said child class.
        '''
        if request.POST.get('send_email_messages'):
        
            '''
            here I am creating a thread that will send the email while I am free to do other 
            things like refreshing the page to improve the UX.
            note that I am not using a non daemon thread, so it finishes in the background.
            '''
            
            io_op = Thread(target=self.email_io_operation, args=(request,))
            io_op.start()
            
        return self.get(request)





# path('home/', IndexView.as_view(), name='home_view')
class IndexView(MyCustomMixin, View):
    template_name = 'main/index.html'
    queryset1 = Cause.objects.filter(Q(event_date=None) | Q(event_date__gt=timezone.now()))
    queryset2 = Donation.objects.all()[:3]
    queryset3 = Event.objects.all().order_by('-date')[:3]
    queryset4 = Post.objects.all()[:3]
    queryset5 = Video.objects.all()




# path('about/', AboutView.as_view(), name='about_view')
class AboutView(MyCustomMixin, View):
    template_name = 'main/about.html'
    queryset1 = TeamMember.objects.all()




# path('causes/', CausesView.as_view(), name='causes_view')
class CausesView(MyCustomMixin, View):
    template_name = 'main/causes.html'




# path('contact/', ContactView.as_view(), name='contact_view')
class ContactView(MyCustomMixin, View):
    template_name = 'main/contact.html'

    def email_io_operation(self, request):
        '''
        this is just a pure python way of sending an email, 
        *well at least packaging them to be sent under the with block :)
        '''
        
        em1 = MIMEMultipart()
        em1['Subject'] = f"Inquiry from {request.POST.get('contact_name')} - {request.POST.get('contact_subject')}"
        em1.attach(MIMEText(f"""
{" ".join(request.POST.get('contact_name').split(' ')[:2])} contacted us and the message reads as follows:
““
{request.POST.get('contact_message')}
””
""", 'plain'))
        

        em2 = MIMEMultipart()
        em2['From'] = 'AinaAbosede Foundation'
        em2['Subject'] = 'Follow-up on your inquiry to our charity organization'
        em2.attach(MIMEText(f"""
Dear {" ".join(request.POST.get('contact_name').split(' ')[:2])},

We are grateful for your interest in our charity organization, and we appreciate your taking the time to contact us through our website. We have received your message and are eager to assist you in any way we can.

Please be informed that one of our dedicated representatives will be in touch with you within the next 24 hours to discuss your inquiry and answer any questions you might have. We are committed to providing you with the information and support you need and we assure you that we will do our best to address your concerns.

If you have any further questions, please don't hesitate to reach out to us. We look forward to connecting with you soon.

Warm regards,
AinaAbosede Foundation team.
""", 'plain'))
        context = ssl.create_default_context()
        
        '''
        Now onto the main business of the email sending,
        we login and then we send two emails.
            - The site email(basically the site sending an email to itself )
            - The email sent to the person who contacted
        '''
        stdout_logger.info("PROCESSING THE DATA...")
        with smtplib.SMTP_SSL(settings.EMAIL_SERVER, settings.EMAIL_PORT, context=context) as smtp:
            smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            smtp.sendmail(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_USER, em1.as_string())
            to_email = request.POST.get('contact_email') or settings.DEFAULT_TO_EMAIL
            smtp.sendmail(settings.EMAIL_HOST_USER, to_email, em2.as_string())
            activity_logger.info(f"Email sent to {request.POST.get('contact_name')} from the contact page.")
            stdout_logger.info("BOTH EMAILS SENT SUCCESSFULLY !!!")





# path('donate/', DonateView.as_view(), name='donate_view')
class DonateView(MyCustomMixin, View):
    template_name = "main/donate.html"

    def get(self, request, *args, **kwargs):
        queryset = list(Donation.objects.all())
        donations_per_page = 9
        page_number = request.GET.get('page', 1)
        
        custom_range, donations, paginator = PaginateObjects(queryset, page_number, donations_per_page)
        
        context = {'custom_range':custom_range,'donations': donations, 'paginator' :paginator, 'footer_events':self.footer_events}
        
        return render(request, self.template_name, context)




# path('events/', EventView.as_view(), name='events_view')
class EventView(MyCustomMixin, View):
    template_name = 'main/events.html'
    causes = Cause.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = list(Event.objects.all())
        events_per_page = 3
        page_number = request.GET.get('page', 1)
        
        custom_range, events, paginator = PaginateObjects(queryset, page_number, events_per_page)
        
        context = {'causes':self.causes, 'custom_range':custom_range,'events': events, 'paginator' :paginator, 'footer_events':self.footer_events}
        
        return render(request, 'main/events.html', context)




# path('event-single/<int:id>/', Event_Single_View.as_view(), name='event-single_view')
class Event_Single_View(MyCustomMixin, View):
    template_name = 'main/event-single.html'

    def get(self, request, id=1, *args, **kwargs):
        self.context['recent_events'] = Event.objects.all().order_by('-date')[:3]
        
        event = get_object_or_404(Event, id=id)
        self.context ['event'] = event
            
            
        return render(request, self.template_name, self.context)
        
    




# path('events-gallery/', GalleryView.as_view(), name='events-gallery_view')
class GalleryView(MyCustomMixin, View):
    template_name = 'main/gallery.html'

    def get(self, request):
        queryset = Event.objects.all()
        page_number = request.GET.get('page', 1)
        events_per_page = 6

        custom_range, events, paginator = PaginateObjects(queryset, page_number, events_per_page)
        context = {'custom_range':custom_range,'events': events, 'paginator' :paginator, 'footer_events':self.footer_events}
        
        return render(request, 'main/gallery.html', context)





# path('event-single-gallery/<int:id>/', Event_Single_Gallery.as_view(), name='event-single-gallery_view')
class Event_Single_Gallery(MyCustomMixin, View):

    def get(self, request, id, *args, **kwargs):
        event = get_object_or_404(Event, id=id)
        queryset = EventPic.objects.filter(event = event)
        page_number = request.GET.get('pics_page', 1)
        pics_per_page = 8

        custom_range, event_pics, paginator = PaginateObjects(queryset, page_number, pics_per_page)
        
        modified_event_pics = [event_pics[x:x+4] for x in range(0 , (len(event_pics)) , 4) ]
        context = {'event':event, 'custom_range':custom_range,'event_pics': event_pics, 'modified_event_pics':modified_event_pics, 'paginator' :paginator, 'footer_events':self.footer_events}
        
        print(custom_range, event_pics, paginator)
        
        return render(request, 'main/event-single-gallery.html', context)




# path('search_events/', search_events, name='event_ajax-search'),
def search_events(request):
    '''
    this function will perform live searches for events on the site.
    it will probably be called by an ajax post request and return a JsonResponse
    '''
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.POST.get('search_query')
        results = Event.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) | 
            Q(creator__username__icontains=query)
        )

        if results and query:
            output = [{'pk':result.pk, 'name':result.name, 'image':str(result.image.url), 'date':result.date } for result in results ]
        else:
            output = 'No Events match your description...'

        return JsonResponse({'data': output})
    return JsonResponse({})
    
