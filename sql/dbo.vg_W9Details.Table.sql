USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_W9Details]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_W9Details](
	[UserId] [uniqueidentifier] NOT NULL,
	[W9Id] [int] IDENTITY(1,1) NOT NULL,
	[Name] [varchar](50) NOT NULL,
	[BusinessName] [varchar](50) NOT NULL,
	[CompanyType] [varchar](50) NOT NULL,
	[OtherCompanyText] [varchar](50) NOT NULL,
	[Exempt] [bit] NOT NULL,
	[Address] [varchar](50) NOT NULL,
	[City] [varchar](50) NOT NULL,
	[State] [char](2) NOT NULL,
	[ZipCode] [varchar](50) NOT NULL,
	[AccountNumbers] [varchar](50) NOT NULL,
	[EINNumber] [varchar](150) NOT NULL,
	[Item2] [bit] NOT NULL,
	[Email] [varchar](50) NOT NULL,
	[DateCreated] [datetime] NOT NULL,
	[Active] [bit] NOT NULL,
	[VGProductID] [int] NOT NULL,
	[DateModified] [datetime] NULL,
 CONSTRAINT [PK_vg_W9Details] PRIMARY KEY CLUSTERED 
(
	[UserId] ASC,
	[VGProductID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
