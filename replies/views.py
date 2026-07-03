from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ClientReply
from utils.ai_helper import generate_client_reply

@login_required
def reply_list(request):
    replies = ClientReply.objects.filter(user=request.user)
    return render(request, 'replies/list.html', {'replies': replies})

@login_required
def reply_create(request):
    if request.method == 'POST':
        reply = ClientReply.objects.create(
            user=request.user,
            client_message=request.POST.get('client_message'),
            tone=request.POST.get('tone', 'professional')
        )
        messages.success(request, 'Reply created successfully!')
        return redirect('reply_detail', pk=reply.pk)
    return render(request, 'replies/create.html')

@login_required
def reply_detail(request, pk):
    reply = get_object_or_404(ClientReply, pk=pk, user=request.user)
    return render(request, 'replies/detail.html', {'reply': reply})

@login_required
def reply_delete(request, pk):
    reply = get_object_or_404(ClientReply, pk=pk, user=request.user)
    if request.method == 'POST':
        reply.delete()
        messages.success(request, 'Reply deleted successfully!')
        return redirect('reply_list')
    return render(request, 'replies/delete.html', {'reply': reply})

@login_required
def reply_generate(request, pk):
    reply = get_object_or_404(ClientReply, pk=pk, user=request.user)
    
    # Check if user has AI credits
    if request.user.profile.ai_credits <= 0:
        messages.error(request, 'You have no AI credits left. Please contact support.')
        return redirect('reply_detail', pk=reply.pk)
    
    if request.method == 'POST':
        # Generate reply using AI
        generated_content = generate_client_reply(reply)
        
        # Save generated content
        reply.generated_reply = generated_content
        reply.save()
        
        # Deduct 1 AI credit
        request.user.profile.ai_credits -= 1
        request.user.profile.save()
        
        messages.success(request, 'Reply generated successfully! 1 AI credit used.')
        return redirect('reply_detail', pk=reply.pk)
    
    return render(request, 'replies/generate.html', {'reply': reply})