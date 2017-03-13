from course.models import Course, Lecture, CourseMembership
from course.serializers import CourseSerializer, LectureSerializer, CourseMembershipSerializer, \
    CourseUserSerializer
from rest_framework import generics
from rest_framework import permissions



class MemberCourseList(generics.ListCreateAPIView):
    """Return a list of all the courses the current user is connected to, as staff or student.

    Authentication is required"""
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        cm = CourseMembership.objects.create(course=course, user=self.request.user, role='staff')
        cm.save()

    def get_queryset(self):
        return self.request.user.courses


class CourseList(generics.ListAPIView):
    """Return all courses that the student is not connected to.

    Authentication is required"""
    serializer_class = CourseSerializer

    def get_queryset(self):
        return Course.objects.exclude(id__in=self.request.user.courses.values_list('id', flat=True))


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    """Return the course information of the course with the id in the url."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class JoinCourse(generics.CreateAPIView):
    """Adds the request user as a student to the course. Course id is retreived from the url."""
    serializer_class = CourseMembershipSerializer

    def perform_create(self, serializer):
        cm = CourseMembership.objects.create(course=Course.objects.get(id=self.kwargs['pk']), user=self.request.user, role='student')
        cm.save()


class CourseAddMember(generics.CreateAPIView):
    serializer_class = CourseMembershipSerializer

    def perform_create(self, serializer):
        pass


class LectureList(generics.ListCreateAPIView):
    serializer_class = LectureSerializer

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        return Lecture.objects.filter(course=self.kwargs['pk'])


class CourseUserList(generics.ListAPIView):
    serializer_class = CourseUserSerializer
    def get_queryset(self):
        return Course.objects.get(id=self.kwargs['pk']).members
